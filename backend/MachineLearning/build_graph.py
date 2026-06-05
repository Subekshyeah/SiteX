import sqlite3
import pandas as pd
import torch
from torch_geometric.data import HeteroData
import os
import hashlib
import pickle
import networkx as nx
from scipy.spatial import cKDTree
import numpy as np

def build_graph(db_path, output_path):
    print("Connecting to database...")
    conn = sqlite3.connect(db_path)
    
    # 1. Load Places
    print("Loading places...")
    places_df = pd.read_sql_query("""
        SELECT place_id, latitude, longitude, 
               open_hours_score_component, foot_traffic_score_component, 
               composite_score
        FROM place 
        WHERE composite_score IS NOT NULL
    """, conn)
    
    # Map string place_id to integer index
    place_id_to_idx = {pid: i for i, pid in enumerate(places_df['place_id'])}
    
    # Extract place features (x) and targets (y)
    # We fill NA values with 0 or mean
    lat = places_df['latitude'].fillna(0).astype(float).values
    lng = places_df['longitude'].fillna(0).astype(float).values
    open_hrs = places_df['open_hours_score_component'].fillna(50.0).astype(float).values
    foot_traffic = places_df['foot_traffic_score_component'].fillna(50.0).astype(float).values
    
    # Normalize features to roughly [0, 1] or mean 0 std 1
    # For simplicity, divide by 100 or standard scaling
    # Lat/Lng in Kathmandu: Lat ~ 27.7, Lng ~ 85.3
    lat_norm = (lat - 27.7) / 0.1
    lng_norm = (lng - 85.3) / 0.1
    open_hrs_norm = open_hrs / 100.0
    foot_traffic_norm = foot_traffic / 100.0
    
    x_place = torch.tensor(list(zip(lat_norm, lng_norm, open_hrs_norm, foot_traffic_norm)), dtype=torch.float)
    y_place = torch.tensor(places_df['composite_score'].values, dtype=torch.float).view(-1, 1)
    
    # 2. Load Categories
    print("Loading categories...")
    categories_df = pd.read_sql_query("SELECT DISTINCT category_name FROM categories_detailed WHERE category_name IS NOT NULL", conn)
    cat_to_idx = {cat: i for i, cat in enumerate(categories_df['category_name'])}
    
    # Category features can just be their index (for an embedding layer later), or a one-hot vector.
    # We will use simple indices: [num_categories, 1]
    x_category = torch.arange(len(cat_to_idx), dtype=torch.long).view(-1, 1)
    
    # Place <-> Category Edges
    print("Building Place-Category edges...")
    place_cat_df = pd.read_sql_query("SELECT place_id, category_name FROM categories_detailed WHERE category_name IS NOT NULL", conn)
    
    # Filter valid places
    place_cat_df = place_cat_df[place_cat_df['place_id'].isin(place_id_to_idx)]
    
    edge_index_place_cat = torch.tensor([
        [place_id_to_idx[pid] for pid in place_cat_df['place_id']],
        [cat_to_idx[cat] for cat in place_cat_df['category_name']]
    ], dtype=torch.long)
    
    # 3. Load Users / Reviews
    print("Loading users and reviews...")
    # We hash the reviewer_name to create a user ID, as they don't have global IDs
    reviews_df = pd.read_sql_query("SELECT place_id, reviewer_name, rating FROM reviews WHERE reviewer_name IS NOT NULL", conn)
    reviews_df = reviews_df[reviews_df['place_id'].isin(place_id_to_idx)]
    
    unique_users = reviews_df['reviewer_name'].unique()
    user_to_idx = {user: i for i, user in enumerate(unique_users)}
    
    # User features: just index for embedding
    x_user = torch.arange(len(user_to_idx), dtype=torch.long).view(-1, 1)
    
    # User <-> Place Edges
    print("Building User-Place edges...")
    edge_index_user_place = torch.tensor([
        [user_to_idx[u] for u in reviews_df['reviewer_name']],
        [place_id_to_idx[p] for p in reviews_df['place_id']]
    ], dtype=torch.long)
    
    # Edge features (Rating)
    edge_attr_user_place = torch.tensor(reviews_df['rating'].values, dtype=torch.float).view(-1, 1)
    
    conn.close()
    
    # 4. Build HeteroData
    print("Constructing PyG HeteroData...")
    data = HeteroData()
    
    data['place'].x = x_place
    data['place'].y = y_place
    
    data['category'].x = x_category
    data['user'].x = x_user
    
    # Edges
    data['place', 'has_category', 'category'].edge_index = edge_index_place_cat
    # PyG expects undirected or reverse edges for message passing in both directions
    data['category', 'rev_has_category', 'place'].edge_index = edge_index_place_cat[[1, 0]]
    
    data['user', 'reviews', 'place'].edge_index = edge_index_user_place
    data['user', 'reviews', 'place'].edge_attr = edge_attr_user_place
    
    data['place', 'rev_reviews', 'user'].edge_index = edge_index_user_place[[1, 0]]
    data['place', 'rev_reviews', 'user'].edge_attr = edge_attr_user_place

    # 5. Load and Integrate OSMnx Road Graph
    print("Loading OSMnx Road Graph...")
    road_pkl_path = os.path.join(os.path.dirname(db_path), "road_graph_cache_osmnx_osmnx_valley.pkl")
    if os.path.exists(road_pkl_path):
        G_road = pickle.load(open(road_pkl_path, 'rb'))
        
        # Extract road nodes
        road_nodes = list(G_road.nodes(data=True))
        road_id_to_idx = {node[0]: i for i, node in enumerate(road_nodes)}
        
        road_lats = []
        road_lngs = []
        road_street_counts = []
        
        for node_id, data_dict in road_nodes:
            road_lats.append((data_dict.get('y', 27.7) - 27.7) / 0.1)
            road_lngs.append((data_dict.get('x', 85.3) - 85.3) / 0.1)
            road_street_counts.append(data_dict.get('street_count', 1))
            
        x_road = torch.tensor(list(zip(road_lats, road_lngs, road_street_counts)), dtype=torch.float)
        data['road_node'].x = x_road
        
        # Extract road edges (street segments)
        road_edges = list(G_road.edges())
        edge_index_road_road = torch.tensor([
            [road_id_to_idx[u] for u, v in road_edges if u in road_id_to_idx and v in road_id_to_idx],
            [road_id_to_idx[v] for u, v in road_edges if u in road_id_to_idx and v in road_id_to_idx]
        ], dtype=torch.long)
        
        data['road_node', 'connected_to', 'road_node'].edge_index = edge_index_road_road
        # Add reverse edges for PyG
        data['road_node', 'rev_connected_to', 'road_node'].edge_index = edge_index_road_road[[1, 0]]
        
        # Map Places to nearest Road Nodes using KDTree
        print("Mapping Places to nearest Road Nodes...")
        road_coords = np.array([[data_dict.get('y', 27.7), data_dict.get('x', 85.3)] for _, data_dict in road_nodes])
        kdtree = cKDTree(road_coords)
        
        # Original lat/lng from the dataframe
        place_coords = np.array(list(zip(lat, lng)))
        
        # Query 3 nearest road nodes for each place
        k = min(3, len(road_nodes))
        distances, indices = kdtree.query(place_coords, k=k)
        
        place_idx_list = []
        road_idx_list = []
        
        for i in range(len(place_coords)):
            for j in range(k):
                place_idx_list.append(i)
                road_idx_list.append(indices[i][j])
                
        edge_index_place_road = torch.tensor([place_idx_list, road_idx_list], dtype=torch.long)
        
        data['place', 'near', 'road_node'].edge_index = edge_index_place_road
        data['road_node', 'rev_near', 'place'].edge_index = edge_index_place_road[[1, 0]]
        print("Road graph integration successful!")
    else:
        print(f"Warning: Road graph pickle not found at {road_pkl_path}. Skipping integration.")

    print(data)
    
    print(f"Saving graph to {output_path}...")
    torch.save(data, output_path)
    
    # Save mappings for later use
    torch.save({
        'place_to_idx': place_id_to_idx,
        'cat_to_idx': cat_to_idx,
        'user_to_idx': user_to_idx
    }, output_path.replace('.pt', '_mappings.pt'))
    
    print("Done!")

if __name__ == "__main__":
    db_file = os.path.join(os.path.dirname(__file__), "..", "DataEngineering", "ktm_all.db")
    out_file = os.path.join(os.path.dirname(__file__), "hetero_graph.pt")
    build_graph(db_file, out_file)
