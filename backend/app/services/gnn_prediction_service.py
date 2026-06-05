import os
import torch
import torch.nn.functional as F
from scipy.spatial import cKDTree
import numpy as np
from pathlib import Path
from typing import Dict, Any
import sys

# Ensure backend directory is in path to import MachineLearning modules
backend_root = str(Path(__file__).resolve().parent.parent.parent)
if backend_root not in sys.path:
    sys.path.append(backend_root)

# Import the model architecture
from MachineLearning.train_gnn import HeteroGNN

class GNNPredictionService:
    _instance = None
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.backend_root = Path(__file__).resolve().parent.parent.parent
        self.ml_dir = self.backend_root / "MachineLearning"
        
        self.model = None
        self.data = None
        self.kdtree = None
        self.road_graph = None
        self.road_nodes_list = None
        self.hidden_dim = 64
        
        self._load_resources()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_resources(self):
        graph_path = self.ml_dir / "hetero_graph.pt"
        model_path = self.ml_dir / "best_hetero_gnn.pth"
        mappings_path = self.ml_dir / "hetero_graph_mappings.pt"
        
        self.idx_to_cat = {}
        self.idx_to_place_id = {}
        if mappings_path.exists():
            mappings = torch.load(mappings_path, map_location='cpu', weights_only=False)
            if 'cat_to_idx' in mappings:
                self.idx_to_cat = {v: k for k, v in mappings['cat_to_idx'].items()}
            if 'place_id_to_idx' in mappings:
                self.idx_to_place_id = {v: k for k, v in mappings['place_id_to_idx'].items()}
        
        import pickle
        road_pkl_path = self.backend_root / "DataEngineering" / "road_graph_cache_osmnx_osmnx_valley.pkl"
        if road_pkl_path.exists():
            print(f"Loading road pkl file from {road_pkl_path} for logging...")
            with open(road_pkl_path, "rb") as f:
                self.road_graph = pickle.load(f)
                self.road_nodes_list = list(self.road_graph.nodes(data=True))
                print(f"Loaded road graph for logging with {len(self.road_nodes_list)} nodes.")
        
        if not graph_path.exists():
            print(f"Warning: Graph not found at {graph_path}")
            return
            
        print("Loading HeteroGNN graph...")
        self.data = torch.load(graph_path, map_location=self.device, weights_only=False)
        
        # Initialize the new SAGEConv HeteroGNN architecture
        self.model = HeteroGNN(
            metadata=self.data.metadata(),
            hidden_channels=self.hidden_dim,
            out_channels=1, 
            num_layers=2
        ).to(self.device)
        
        if model_path.exists():
            print("Loading HeteroGNN weights...")
            checkpoint = torch.load(model_path, map_location=self.device)
            # Handle both old combined format and new pure state_dict format
            if isinstance(checkpoint, dict) and 'model' in checkpoint:
                self.model.load_state_dict(checkpoint['model'], strict=False)
                print("Loaded model from combined checkpoint (ignoring external embeddings).")
            else:
                # The new pure state dict format
                self.model.load_state_dict(checkpoint)
                print("Loaded model from pure state_dict checkpoint.")
            self.model.eval()
        else:
            print(f"Warning: Model weights not found at {model_path}")
            
        # Build KDTree for road nodes for spatial queries
        if 'road_node' in self.data.node_types:
            # Reconstruct lat/lng from normalized x features
            road_x = self.data['road_node'].x.numpy()
            road_lats = (road_x[:, 0] * 0.1) + 27.7
            road_lngs = (road_x[:, 1] * 0.1) + 85.3
            
            road_coords = np.column_stack((road_lats, road_lngs))
            self.kdtree = cKDTree(road_coords)

    def predict(self, lat: float, lng: float) -> Dict[str, Any]:
        if self.model is None or self.data is None:
            raise RuntimeError("Model or graph not loaded properly.")
            
        # 1. Normalize lat/lng (using same scaling as build_graph.py)
        lat_norm = (lat - 27.7) / 0.1
        lng_norm = (lng - 85.3) / 0.1
        
        orig_place_x = self.data['place'].x
        
        # Dynamically create new_place_x using the mean of existing places to handle N dimensions safely
        new_place_x = orig_place_x.mean(dim=0, keepdim=True).to(self.device)
        # Override lat and lng (assuming they are at index 0 and 1)
        new_place_x[0, 0] = lat_norm
        new_place_x[0, 1] = lng_norm
        
        # 2. Add node temporarily to graph
        self.data['place'].x = torch.cat([orig_place_x, new_place_x], dim=0)
        
        new_place_idx = self.data['place'].x.size(0) - 1
        
        orig_near_edges = None
        orig_rev_near_edges = None
        
        # 3. Find 3 nearest road nodes and add temporary edges
        if ('place', 'near', 'road_node') in self.data.edge_types:
            orig_near_edges = self.data['place', 'near', 'road_node'].edge_index
            orig_rev_near_edges = self.data['road_node', 'rev_near', 'place'].edge_index
        else:
            # Handle case where user also renamed or removed near edges
            orig_near_edges = torch.empty((2, 0), dtype=torch.long)
            orig_rev_near_edges = torch.empty((2, 0), dtype=torch.long)
            
        orig_place_cat_edges = self.data['place', 'has_category', 'category'].edge_index
        orig_rev_place_cat_edges = self.data['category', 'rev_has_category', 'place'].edge_index
        
        if self.kdtree is not None:
            distances, indices = self.kdtree.query([[lat, lng]], k=3)
            
            # --- LOGGING ROAD NEIGHBORS ---
            if self.road_graph is not None and self.road_nodes_list is not None:
                print(f"\n[{lat:.6f}, {lng:.6f}] Connecting to {len(indices[0])} nearest road nodes:")
                for i, r_idx in enumerate(indices[0]):
                    node_id, node_data = self.road_nodes_list[r_idx]
                    street_count = node_data.get('street_count', 0)
                    connected_edges = list(self.road_graph.edges(node_id, data=True))
                    highway_types = set()
                    for u, v, e_data in connected_edges:
                        hw = e_data.get('highway', 'unknown')
                        if isinstance(hw, list):
                            highway_types.update(hw)
                        else:
                            highway_types.add(hw)
                    dist_deg = distances[0][i]
                    print(f"  -> Road Node {i+1}: Intersections: {street_count}, Distance: {dist_deg:.5f} deg, Types: {', '.join(highway_types)}")
            # ------------------------------
            
            place_idx_list = [new_place_idx, new_place_idx, new_place_idx]
            road_idx_list = indices[0].tolist()
            
            new_edges = torch.tensor([place_idx_list, road_idx_list], dtype=torch.long).to(self.device)
            
            self.data['place', 'near', 'road_node'].edge_index = torch.cat(
                [orig_near_edges, new_edges], dim=1
            )
            
            new_rev_edges = torch.tensor([road_idx_list, place_idx_list], dtype=torch.long).to(self.device)
            self.data['road_node', 'rev_near', 'place'].edge_index = torch.cat(
                [orig_rev_near_edges, new_rev_edges], dim=1
            )
            
        # 4. Also link the new node to the most common categories from its nearest existing places
        # Find the 5 nearest existing places using the place KDTree
        place_x_np = orig_place_x.numpy()
        place_lats = (place_x_np[:, 0] * 0.1) + 27.7
        place_lngs = (place_x_np[:, 1] * 0.1) + 85.3
        place_coords_np = np.column_stack((place_lats, place_lngs))
        place_kdtree = cKDTree(place_coords_np)
        distances_place, nearest_place_indices = place_kdtree.query([[lat, lng]], k=5)
        nearest_place_indices = nearest_place_indices[0].tolist()
        
        # Find all categories connected to these nearby places
        edge_src = orig_place_cat_edges[0]  # place indices
        edge_dst = orig_place_cat_edges[1]  # category indices
        
        print(f"\n[{lat:.6f}, {lng:.6f}] Connecting to 5 nearest place nodes:")
        nearby_cats_all = []
        for i, pi in enumerate(nearest_place_indices):
            mask = (edge_src == pi)
            cats_for_place = edge_dst[mask].tolist()
            nearby_cats_all.extend(cats_for_place)
            
            p_lat = place_lats[pi]
            p_lng = place_lngs[pi]
            dist_deg = distances_place[0][i]
            
            place_id = self.idx_to_place_id.get(pi, f"Unknown_{pi}")
            cat_names = [self.idx_to_cat.get(c, str(c)) for c in cats_for_place]
            
            print(f"  -> Place Node {i+1} (ID: {place_id}) at [{p_lat:.5f}, {p_lng:.5f}]:")
            print(f"       Distance: {dist_deg:.5f} deg")
            print(f"       Categories ({len(cat_names)}): {', '.join(cat_names)}")
            
        nearby_cats = list(set(nearby_cats_all))[:5]  # unique, up to 5
        inherited_cat_names = [self.idx_to_cat.get(c, str(c)) for c in nearby_cats]
        print(f"  => Inheriting {len(nearby_cats)} unique categories: {', '.join(inherited_cat_names)}\n")
        
        if nearby_cats:
            new_place_cat_src = [new_place_idx] * len(nearby_cats)
            new_cat_place_src = nearby_cats
            new_place_cat_edges = torch.tensor([new_place_cat_src, new_cat_place_src], dtype=torch.long).to(self.device)
            self.data['place', 'has_category', 'category'].edge_index = torch.cat(
                [orig_place_cat_edges, new_place_cat_edges], dim=1
            )
            new_rev_cat_edges = torch.tensor([new_cat_place_src, new_place_cat_src], dtype=torch.long).to(self.device)
            self.data['category', 'rev_has_category', 'place'].edge_index = torch.cat(
                [orig_rev_place_cat_edges, new_rev_cat_edges], dim=1
            )
            
        # 4. Prepare node features dict for forward pass
        x_dict = {
            'place': self.data['place'].x.to(self.device),
        }
        if 'road_node' in self.data.node_types:
            x_dict['road_node'] = self.data['road_node'].x.to(self.device)
            
        # The new HeteroGNN class handles category embeddings internally inside its input_proj ModuleDict
        # We just need to pass the raw index tensor
        if 'category' in self.data.node_types:
            x_dict['category'] = self.data['category'].x.to(self.device)
        
        # 5. Forward Pass
        with torch.no_grad():
            out = self.model(x_dict, self.data.edge_index_dict)
            
        # The predicted score for the new place
        # The model output was divided by 100 during training (target was y/100.0)
        # So we multiply by 100 to get it back to 0-100 scale. We also clamp to [0, 100].
        predicted_score = float(out[-1].item()) * 100.0
        predicted_score = max(0.0, min(100.0, predicted_score))
        
        # Restore graph to original state (cleanup)
        self.data['place'].x = orig_place_x
        if orig_near_edges is not None:
            self.data['place', 'near', 'road_node'].edge_index = orig_near_edges
            self.data['road_node', 'rev_near', 'place'].edge_index = orig_rev_near_edges
        self.data['place', 'has_category', 'category'].edge_index = orig_place_cat_edges
        self.data['category', 'rev_has_category', 'place'].edge_index = orig_rev_place_cat_edges
            
        # 6. Risk assessment
        if predicted_score < 40.0:
            risk_level = 'High'
        elif predicted_score < 70.0:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
            
        return {
            "predicted_score": predicted_score,
            "risk_level": risk_level,
            "estimated_features": {"lat": lat, "lng": lng, "injected_graph": True}
        }
