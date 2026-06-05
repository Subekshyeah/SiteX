import nbformat as nbf
import os

nb_path = 'd:/projects/Finalproject/SiteX/backend/MachineLearning/hetero_gnn_workflow.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# find the Markdown cell "## 2. Model Training"
insert_idx = -1
for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'markdown' and '2. Model Training' in cell.source:
        insert_idx = i + 1
        break

if insert_idx != -1:
    # check if the next cell is already the training cell
    if insert_idx < len(nb.cells) and nb.cells[insert_idx].cell_type == 'code' and 'class HeteroGNN' in nb.cells[insert_idx].source:
        print("Training cell already exists. Replacing it.")
        nb.cells.pop(insert_idx)
    
    source = """import os
import torch
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.loader import NeighborLoader
from torch_geometric.nn import HGTConv, Linear
import matplotlib.pyplot as plt

class HeteroGNN(torch.nn.Module):
    def __init__(self, metadata, hidden_channels, out_channels, num_layers):
        super().__init__()
        
        self.lin_dict = torch.nn.ModuleDict()
        self.lin_dict['place'] = Linear(-1, hidden_channels)
        self.lin_dict['road_node'] = Linear(-1, hidden_channels)
        
        # HGT layers
        self.convs = torch.nn.ModuleList()
        for _ in range(num_layers):
            conv = HGTConv(hidden_channels, hidden_channels, metadata, heads=4)
            self.convs.append(conv)
            
        # Prediction head
        self.head = Linear(hidden_channels, out_channels)
        
    def forward(self, x_dict, edge_index_dict):
        out_dict = {}
        for node_type, x in x_dict.items():
            if node_type in self.lin_dict:
                out_dict[node_type] = self.lin_dict[node_type](x)
            else:
                out_dict[node_type] = x 
                
        # Message passing
        for conv in self.convs:
            out_dict = conv(out_dict, edge_index_dict)
            out_dict = {key: F.elu(x) for key, x in out_dict.items()}
            
        return self.head(out_dict['place'])

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    graph_path = "hetero_graph.pt"
    if not os.path.exists(graph_path):
        print("Graph not found.")
        return
        
    data = torch.load(graph_path, weights_only=False)
    print(data)
    
    num_users = data['user'].x.size(0)
    num_categories = data['category'].x.size(0)
    hidden_dim = 64
    
    user_emb = torch.nn.Embedding(num_users, hidden_dim)
    cat_emb = torch.nn.Embedding(num_categories, hidden_dim)
    
    num_places = data['place'].num_nodes
    torch.manual_seed(42)
    perm = torch.randperm(num_places)
    
    train_idx = perm[:int(0.8 * num_places)]
    val_idx = perm[int(0.8 * num_places):int(0.9 * num_places)]
    test_idx = perm[int(0.9 * num_places):]
    
    train_mask = torch.zeros(num_places, dtype=torch.bool)
    val_mask = torch.zeros(num_places, dtype=torch.bool)
    test_mask = torch.zeros(num_places, dtype=torch.bool)
    
    train_mask[train_idx] = True
    val_mask[val_idx] = True
    test_mask[test_idx] = True
    
    data['place'].train_mask = train_mask
    data['place'].val_mask = val_mask
    data['place'].test_mask = test_mask

    # To save memory, we apply embeddings to user and category FIRST
    # because they don't have feature matrices, just indices.
    # But NeighborLoader samples subgraphs, so we need to embed the sampled indices.
    # Wait, HGTConv expects actual features. 
    # For NeighborLoader, the sampled batch will have `data['user'].x` containing the sampled indices.
    # We will pass those through the embedding layer inside the training loop.
    
    # We'll use full batch training since NeighborLoader requires pyg-lib or torch-sparse
    # which are hard to install on Windows without C++ build tools.
    data = data.to(device)

    model = HeteroGNN(
        metadata=data.metadata(),
        hidden_channels=hidden_dim,
        out_channels=1, 
        num_layers=2
    ).to(device)
    
    user_emb = user_emb.to(device)
    cat_emb = cat_emb.to(device)
    
    optimizer = torch.optim.Adam(
        list(model.parameters()) + list(user_emb.parameters()) + list(cat_emb.parameters()), 
        lr=0.005
    )
    
    best_val_rmse = float('inf')
    
    print("Starting Training (Full-Batch)...")
    
    for epoch in range(1, 51):
        model.train()
        optimizer.zero_grad()
        
        # Embed categorical nodes
        x_dict = {
            'place': data['place'].x,
        }
        if 'road_node' in data.node_types:
            x_dict['road_node'] = data['road_node'].x
            
        x_dict['category'] = cat_emb(data['category'].x.squeeze(-1))
        x_dict['user'] = user_emb(data['user'].x.squeeze(-1))
        
        out = model(x_dict, data.edge_index_dict)
        
        y_true = data['place'].y / 100.0
        
        # Calculate loss only on training nodes
        train_mask = data['place'].train_mask
        loss = F.mse_loss(out[train_mask], y_true[train_mask])
        loss.backward()
        optimizer.step()
        
        # Validation
        model.eval()
        with torch.no_grad():
            out = model(x_dict, data.edge_index_dict)
            val_mask = data['place'].val_mask
            val_loss = F.mse_loss(out[val_mask], y_true[val_mask])
            val_rmse = (val_loss.item() ** 0.5) * 100.0

        
        if val_rmse < best_val_rmse:
            best_val_rmse = val_rmse
            torch.save({
                'model': model.state_dict(),
                'user_emb': user_emb.state_dict(),
                'cat_emb': cat_emb.state_dict(),
            }, "best_hetero_gnn.pth")
            
        print(f'Epoch: {epoch:03d}, Train Loss: {loss.item():.4f}, Val RMSE: {val_rmse:.2f} points')
        
    print("Done!")

train()"""
    
    new_cell = nbf.v4.new_code_cell(source=source)
    new_cell.id = "445953b9"
    nb.cells.insert(insert_idx, new_cell)
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Restored cell at index {insert_idx}")
else:
    print("Could not find '2. Model Training' markdown cell.")
