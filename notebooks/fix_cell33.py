import sys
import json

nb_path = 'd:/projects/Finalproject/SiteX/notebooks/sentiment_analysis_workflow.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

src = nb['cells'][33]['source']
new_src = []
for line in src:
    if 'SELECT place_id, title' in line:
        line = line.replace('title', 'place AS title')
    
    if "merged_analyzed = merged_merged[merged_merged['sentiment_review_count'].notna()].copy()" in line:
        continue
        
    new_src.append(line)

nb['cells'][33]['source'] = new_src

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('✅ Fixed Cell 33 to include ALL places.')
