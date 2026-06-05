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
        _, nearest_place_indices = place_kdtree.query([[lat, lng]], k=5)
        nearest_place_indices = nearest_place_indices[0].tolist()
        
        # Find all categories connected to these nearby places
        edge_src = orig_place_cat_edges[0]  # place indices
        edge_dst = orig_place_cat_edges[1]  # category indices
        nearby_cats = []
        for pi in nearest_place_indices:
            mask = (edge_src == pi)
            nearby_cats.extend(edge_dst[mask].tolist())
        nearby_cats = list(set(nearby_cats))[:5]  # unique, up to 5
        
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
