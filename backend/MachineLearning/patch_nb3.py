import nbformat as nbf

nb_path = 'hetero_gnn_workflow.ipynb'
with open(nb_path, 'r') as f:
    nb = nbf.read(f, as_version=4)

# Find and replace the test/inference cell that loads best_hetero_gnn.pth incorrectly
for i, cell in enumerate(nb.cells):
    if cell.cell_type != 'code':
        continue
    if 'best_hetero_gnn.pth' in cell.source and 'model.load_state_dict' in cell.source:
        cell.source = cell.source.replace(
            "model.load_state_dict(torch.load('best_hetero_gnn.pth', map_location=device))",
            """checkpoint = torch.load('best_hetero_gnn.pth', map_location=device)
if isinstance(checkpoint, dict) and 'model' in checkpoint:
    model.load_state_dict(checkpoint['model'])
    user_emb.load_state_dict(checkpoint['user_emb'])
    cat_emb.load_state_dict(checkpoint['cat_emb'])
    print("Loaded combined checkpoint (model + embeddings).")
else:
    model.load_state_dict(checkpoint)
    print("Loaded legacy checkpoint (embeddings are random).")"""
        )
        print(f"Patched test cell {i}")

with open(nb_path, 'w') as f:
    nbf.write(nb, f)
print('Done.')
