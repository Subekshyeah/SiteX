import nbformat as nbf

nb_path = 'd:/projects/Finalproject/SiteX/backend/MachineLearning/hetero_gnn_workflow.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

for i, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'build_graph' in cell.source:
        has_leak = 'sentiment_score_component' in cell.source
        print(f'Cell {i}: has_leak={has_leak}, first 80 chars: {repr(cell.source[:80])}')
