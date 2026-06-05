import nbformat as nbf

nb_path = 'd:/projects/Finalproject/SiteX/backend/MachineLearning/hetero_gnn_workflow.ipynb'
with open(nb_path, 'r') as f:
    nb = nbf.read(f, as_version=4)

for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'model.load_state_dict' in cell.source and 'test_lat, test_lng' in cell.source:
        cell.source = """from train_gnn import HeteroGNN
import torch
import numpy as np
from scipy.spatial import cKDTree

# 1. Load the graph and model weights
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
data = torch.load('hetero_graph.pt', map_location=device, weights_only=False)

# Assuming user and category count didn't change since training
num_users = data['user'].x.size(0)
num_categories = data['category'].x.size(0)
hidden_dim = 64

user_emb = torch.nn.Embedding(num_users, hidden_dim).to(device)
cat_emb = torch.nn.Embedding(num_categories, hidden_dim).to(device)

model = HeteroGNN(
    metadata=data.metadata(),
    hidden_channels=hidden_dim,
    out_channels=1, 
    num_layers=2
).to(device)
checkpoint = torch.load('best_hetero_gnn.pth', map_location=device)
if isinstance(checkpoint, dict) and 'model' in checkpoint:
    model.load_state_dict(checkpoint['model'])
    user_emb.load_state_dict(checkpoint['user_emb'])
    cat_emb.load_state_dict(checkpoint['cat_emb'])
    print("Loaded combined checkpoint (model + embeddings).")
else:
    model.load_state_dict(checkpoint)
    print("Loaded legacy checkpoint (embeddings are random).")
model.eval()

# 2. Find the nearest EXISTING place in the graph
test_lat, test_lng = 27.749976099999998, 85.3468032

place_x_np = data['place'].x.numpy()
place_lats = (place_x_np[:, 0] * 0.1) + 27.7
place_lngs = (place_x_np[:, 1] * 0.1) + 85.3
place_coords_np = np.column_stack((place_lats, place_lngs))
place_kdtree = cKDTree(place_coords_np)

distance, place_idx = place_kdtree.query([[test_lat, test_lng]], k=1)
place_idx = place_idx[0]

# 3. Get the model's prediction for the entire graph (without injecting a new node)
x_dict = {
    'place': data['place'].x.to(device),
}
if 'road_node' in data.node_types:
    x_dict['road_node'] = data['road_node'].x.to(device)
    
x_dict['category'] = cat_emb(data['category'].x.squeeze(-1).to(device))
x_dict['user'] = user_emb(data['user'].x.squeeze(-1).to(device))

with torch.no_grad():
    out = model(x_dict, data.edge_index_dict)

predicted_score = max(0.0, min(100.0, float(out[place_idx].item()) * 100.0))
actual_score = float(data['place'].y[place_idx].item())

print(f"Nearest Existing Place Index: {place_idx}")
print(f"Actual Composite Score in Graph: {actual_score:.2f}")
print(f"Model's Predicted Score: {predicted_score:.2f}")
"""
        print(f"Patched test cell {i}")

with open(nb_path, 'w') as f:
    nbf.write(nb, f)
print('Done.')
