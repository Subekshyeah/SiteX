import nbformat as nbf
import os

nb_path = 'd:/projects/Finalproject/SiteX/backend/MachineLearning/hetero_gnn_workflow.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

patched = False
for cell in nb.cells:
    if cell.cell_type == 'code' and 'ReduceLROnPlateau' in cell.source:
        # PyTorch 2.2+ removed the verbose flag from schedulers
        if 'verbose=True' in cell.source:
            cell.source = cell.source.replace("verbose=True", "")
            patched = True
        elif 'verbose=False' in cell.source:
            cell.source = cell.source.replace("verbose=False", "")
            patched = True

if patched:
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Successfully removed 'verbose' argument from ReduceLROnPlateau.")
else:
    print("Could not find 'verbose' argument to remove.")
