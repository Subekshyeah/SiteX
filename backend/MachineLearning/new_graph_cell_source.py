import sqlite3
import pandas as pd
import numpy as np
import torch
import pickle
import os

from torch_geometric.data import HeteroData
from scipy.spatial import cKDTree


def build_graph(db_path, road_pkl_path, output_path):

    print("Connecting to database...")
    conn = sqlite3.connect(db_path)

    # ─────────────────────────────────────────────────────────────
    # 1. Load Places — only NON-LEAKY features
    # We deliberately exclude review-derived score components
    # (sentiment, rating, volume) because they directly encode the
    # composite_score target, causing trivial feature leakage.
    # Kept: lat, lng (geography) + open_hours, foot_traffic (external signals)
    # ─────────────────────────────────────────────────────────────
    print("Loading places...")

    places_df = pd.read_sql_query(
        (
            "SELECT p.place_id, p.latitude, p.longitude, "
            "p.foot_traffic_score_component, p.open_hours_score_component, "
            "p.composite_score "
            "FROM place p "
            "WHERE p.composite_score IS NOT NULL "
            "AND p.latitude IS NOT NULL "
            "AND p.longitude IS NOT NULL"
        ),
        conn
    )

    print(f"Loaded {len(places_df):,} places")

    fill_defaults = {
        "foot_traffic_score_component": 50.0,
        "open_hours_score_component":   50.0,
    }
    places_df = places_df.fillna(fill_defaults)

    place_id_to_idx = {
        pid: i
        for i, pid in enumerate(places_df["place_id"])
    }

    lat = places_df["latitude"].values.astype(float)
    lng = places_df["longitude"].values.astype(float)

    # ─────────────────────────────────────────────────────────────
    # Feature normalization  (4 features — NO leakage)
    # ─────────────────────────────────────────────────────────────

    lat_norm          = (lat - 27.7) / 0.1
    lng_norm          = (lng - 85.3) / 0.1
    open_hrs_norm     = places_df["open_hours_score_component"].values   / 100.0
    foot_traffic_norm = places_df["foot_traffic_score_component"].values / 100.0

    # Stack into [N, 4] feature matrix
    x_place = torch.tensor(
        np.column_stack([
            lat_norm,
            lng_norm,
            open_hrs_norm,
            foot_traffic_norm,
        ]),
        dtype=torch.float
    )

    # Target normalized to [0, 1]
    y_place = torch.tensor(
        places_df["composite_score"].values / 100.0,
        dtype=torch.float
    ).view(-1, 1)

    print(f"Place feature matrix: {x_place.shape}  (4 clean features, no leakage)")
    print(
        f"Score range: "
        f"{places_df['composite_score'].min():.1f} "
        f"to "
        f"{places_df['composite_score'].max():.1f}"
    )

    # ─────────────────────────────────────────────────────────────
    # 2. Load Categories
    # ─────────────────────────────────────────────────────────────
    print("Loading categories...")

    categories_df = pd.read_sql_query(
        (
            "SELECT DISTINCT category_name "
            "FROM categories_detailed "
            "WHERE category_name IS NOT NULL"
        ),
        conn
    )

    cat_to_idx = {
        cat: i
        for i, cat in enumerate(categories_df["category_name"])
    }

    x_category = torch.arange(
        len(cat_to_idx),
        dtype=torch.long
    ).view(-1, 1)

    print(f"{len(cat_to_idx):,} unique categories")

    place_cat_df = pd.read_sql_query(
        (
            "SELECT place_id, category_name "
            "FROM categories_detailed "
            "WHERE category_name IS NOT NULL"
        ),
        conn
    )

    place_cat_df = place_cat_df[
        place_cat_df["place_id"].isin(place_id_to_idx)
    ]

    edge_place_cat = torch.tensor(
        [
            [place_id_to_idx[p] for p in place_cat_df["place_id"]],
            [cat_to_idx[c]      for c in place_cat_df["category_name"]]
        ],
        dtype=torch.long
    )

    print(f"Place-Category edges: {edge_place_cat.shape[1]:,}")

    conn.close()

    # ─────────────────────────────────────────────────────────────
    # 3. Build HeteroData
    # ─────────────────────────────────────────────────────────────
    print("Constructing HeteroData...")

    data = HeteroData()

    data["place"].x         = x_place
    data["place"].y         = y_place
    data["place"].place_ids = list(places_df["place_id"])

    data["category"].x = x_category

    data["place", "has_category", "category"].edge_index     = edge_place_cat
    data["category", "rev_has_category", "place"].edge_index = edge_place_cat[[1, 0]]

    # ─────────────────────────────────────────────────────────────
    # 4. Load Road Graph
    # ─────────────────────────────────────────────────────────────
    print("Loading road graph...")

    if os.path.exists(road_pkl_path):

        with open(road_pkl_path, "rb") as f:
            G_road = pickle.load(f)

        road_nodes = list(G_road.nodes(data=True))

        road_id_to_idx = {node[0]: i for i, node in enumerate(road_nodes)}

        road_lats    = [(d.get("y", 27.7) - 27.7) / 0.1 for _, d in road_nodes]
        road_lngs    = [(d.get("x", 85.3) - 85.3) / 0.1 for _, d in road_nodes]
        street_cnts  = [min(d.get("street_count", 1), 8) / 8.0 for _, d in road_nodes]

        data["road_node"].x = torch.tensor(
            list(zip(road_lats, road_lngs, street_cnts)),
            dtype=torch.float
        )

        valid_edges = [
            (u, v) for u, v in G_road.edges()
            if u in road_id_to_idx and v in road_id_to_idx
        ]

        if valid_edges:
            src = [road_id_to_idx[u] for u, v in valid_edges]
            dst = [road_id_to_idx[v] for u, v in valid_edges]
            edge_road = torch.tensor([src, dst], dtype=torch.long)

            data["road_node", "connected_to",     "road_node"].edge_index = edge_road
            data["road_node", "rev_connected_to", "road_node"].edge_index = edge_road[[1, 0]]

        # Place -> nearest road nodes (k=5)
        road_coords  = np.array([[d.get("y", 27.7), d.get("x", 85.3)] for _, d in road_nodes])
        place_coords = np.column_stack([lat, lng])

        kdtree = cKDTree(road_coords)
        k = min(5, len(road_nodes))
        dists, idxs = kdtree.query(place_coords, k=k)

        p_list, r_list = [], []
        for i in range(len(place_coords)):
            for j in range(k):
                p_list.append(i)
                r_list.append(idxs[i][j])

        edge_place_road = torch.tensor([p_list, r_list], dtype=torch.long)

        data["place",     "near",     "road_node"].edge_index = edge_place_road
        data["road_node", "rev_near", "place"].edge_index     = edge_place_road[[1, 0]]

        print(f"Road nodes: {len(road_nodes):,}, edges: {len(valid_edges):,}")

    else:
        print(f"WARNING: Road graph not found at {road_pkl_path} — skipping")

    print("\nFinal graph:")
    print(data)

    # ─────────────────────────────────────────────────────────────
    # 5. Save
    # ─────────────────────────────────────────────────────────────
    torch.save(data, output_path)

    torch.save(
        {"place_id_to_idx": place_id_to_idx, "cat_to_idx": cat_to_idx},
        output_path.replace(".pt", "_mappings.pt")
    )

    print(f"\nSaved to {output_path}")
    return data


# ─────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.getcwd(), "..", "DataEngineering", "ktm_all.db")

ROAD_PKL_PATH = os.path.join(
    os.getcwd(), "..", "DataEngineering",
    "road_graph_cache_osmnx_osmnx_valley.pkl"
)

OUT_PATH = os.path.join(os.getcwd(), "hetero_graph.pt")

data = build_graph(DB_PATH, ROAD_PKL_PATH, OUT_PATH)
