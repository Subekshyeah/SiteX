import nbformat as nbf

nb_path = 'd:/projects/Finalproject/SiteX/backend/MachineLearning/hetero_gnn_workflow.ipynb'

# Read the new clean source from file (avoids quoting issues)
with open('new_graph_cell_source.py', 'r', encoding='utf-8') as f:
    new_source = f.read()

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

patched = False
for i, cell in enumerate(nb.cells):
    if (cell.cell_type == 'code'
            and 'build_graph' in cell.source
            and 'sentiment_score_component' in cell.source):
        cell.source = new_source
        cell['outputs'] = []
        cell['execution_count'] = None
        patched = True
        print(f"Patched cell {i} successfully.")
        break

if not patched:
    print("ERROR: Could not find the leaky graph builder cell.")
else:
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Notebook saved.")
