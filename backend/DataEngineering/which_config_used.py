import pandas as pd
from pathlib import Path
import importlib.util

p=Path(r'd:\projects\SiteX\backend\Data\score_entries.py')
spec = importlib.util.spec_from_file_location('scmod', str(p))
scmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scmod)
CONFIG = scmod.CONFIG

csv= pd.read_csv(r'd:\projects\SiteX\backend\Data\CSV\compact_cafe_selected.csv', dtype=str, low_memory=False)
cols = set(csv.columns.tolist())
used = [k for k in CONFIG.keys() if k in cols]
missing = [k for k in CONFIG.keys() if k not in cols]
print('Found in CSV (will be used):')
for k in used:
    print(' -', k)
print('\nConfigured but NOT found in CSV:')
for k in missing:
    print(' -', k)
