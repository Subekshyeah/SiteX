"""GNN sub-package for SiteX.

Modules
-------
graph_builder   Build a heterogeneous graph from the OSMnx road network + POI CSVs.
node_features   Compute per-node feature vectors for each node type.
edge_features   Compute per-edge feature vectors for each edge type.
gnn_model       GraphSAGE / GAT model definition (requires torch + torch_geometric).
"""
