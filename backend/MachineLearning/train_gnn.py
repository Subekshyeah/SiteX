import os
import torch
import torch.nn.functional as F
from torch_geometric.data import HeteroData
from torch_geometric.nn import HeteroConv, SAGEConv, Linear
import matplotlib.pyplot as plt

class HeteroGNN(torch.nn.Module):
    """
    Heterogeneous GNN using SAGEConv message passing.
    Lighter than HGTConv — no multi-head attention across all edge types.
    Processes: place, category, road_node.
    Predicts: composite_score for each place node.
    """
    def __init__(self, metadata, hidden_channels=64, out_channels=1, num_layers=2):
        super().__init__()

        # Input projection: each node type gets its own linear to hidden_channels
        self.input_proj = torch.nn.ModuleDict()
        self.input_proj['place']     = Linear(-1, hidden_channels)  # -1 = infer input dim
        self.input_proj['road_node'] = Linear(-1, hidden_channels)
        self.input_proj['category']  = torch.nn.Embedding(4000, hidden_channels)  # category index embed

        # HeteroConv layers: one per message-passing step
        self.convs = torch.nn.ModuleList()
        for _ in range(num_layers):
            conv = HeteroConv({
                ('place',     'has_category',     'category'): SAGEConv((-1, -1), hidden_channels),
                ('category',  'rev_has_category', 'place'):    SAGEConv((-1, -1), hidden_channels),
                ('place',     'near',             'road_node'): SAGEConv((-1, -1), hidden_channels),
                ('road_node', 'rev_near',          'place'):    SAGEConv((-1, -1), hidden_channels),
                ('road_node', 'connected_to',     'road_node'): SAGEConv((-1, -1), hidden_channels),
                ('road_node', 'rev_connected_to', 'road_node'): SAGEConv((-1, -1), hidden_channels),
            }, aggr='sum')
            self.convs.append(conv)

        self.bn = torch.nn.BatchNorm1d(hidden_channels)  # stabilizes training
        self.dropout = torch.nn.Dropout(p=0.2)
        self.head = torch.nn.Sequential(
            Linear(hidden_channels, 32),
            torch.nn.ReLU(),
            Linear(32, out_channels),
            torch.nn.Sigmoid()  # output in [0, 1], multiply by 100 for score
        )

    def forward(self, x_dict, edge_index_dict):
        # Project each node type to hidden dim
        h = {}
        for node_type, x in x_dict.items():
            if node_type == 'category':
                h[node_type] = self.input_proj['category'](x.squeeze(-1).long())
            elif node_type in self.input_proj:
                h[node_type] = self.input_proj[node_type](x.float())
            else:
                h[node_type] = x.float()  # passthrough if not projected

        # Message passing
        for i, conv in enumerate(self.convs):
            h = conv(h, edge_index_dict)
            h = {k: F.elu(v) for k, v in h.items()}

        # Apply BN + dropout to place embeddings only
        place_emb = self.bn(h['place'])
        place_emb = self.dropout(place_emb)

        return self.head(place_emb)

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    graph_path = os.path.join(os.path.dirname(__file__), "hetero_graph.pt")
    if not os.path.exists(graph_path):
        print("Graph not found.")
        return
        
    data = torch.load(graph_path, weights_only=False)
    print(data)
    
    hidden_dim = 64
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

    data = data.to(device)

    model = HeteroGNN(
        metadata=data.metadata(),
        hidden_channels=hidden_dim,
        out_channels=1, 
        num_layers=2
    ).to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', patience=10, factor=0.5
    )
    
    best_val_rmse = float('inf')
    x_dict = dict(data.x_dict)
    
    print("Starting Training (Full-Batch)...")
    
    for epoch in range(1, 101):
        model.train()
        optimizer.zero_grad()
        
        out = model(x_dict, data.edge_index_dict)
        y_true = data['place'].y
        
        loss = F.mse_loss(out[train_mask], y_true[train_mask])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        
        model.eval()
        with torch.no_grad():
            out_eval = model(x_dict, data.edge_index_dict)
            val_mse = F.mse_loss(out_eval[val_mask], y_true[val_mask]).item()
            val_rmse = (val_mse ** 0.5) * 100.0

        scheduler.step(val_mse)
        
        if val_rmse < best_val_rmse:
            best_val_rmse = val_rmse
            # Only save model state dict, no separate embeddings needed
            torch.save(model.state_dict(), os.path.join(os.path.dirname(__file__), "best_hetero_gnn.pth"))
            
        if epoch % 10 == 0 or epoch == 1:
            print(f'Epoch {epoch:03d} | Train Loss: {loss.item():.4f} | Val RMSE: {val_rmse:.2f} pts | LR: {optimizer.param_groups[0]["lr"]:.5f}')
        
    print("Done!")

if __name__ == "__main__":
    train()
