#!/usr/bin/env python3
import csv
from pathlib import Path

orig = Path('comp/csv/compact_summary.csv')
report = Path('comp/csv/generated_report.csv')
out = Path('comp/csv/compact_summary_merged.csv')

# fields in report
one='reviewsDistribution_oneStar'
two='reviewsDistribution_twoStar'
three='reviewsDistribution_threeStar'
four='reviewsDistribution_fourStar'
five='reviewsDistribution_fiveStar'

# Read report into dict keyed by (name, city, rating_str)
rep_map = {}
with report.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        key = (r.get('name','').strip(), r.get('city','').strip(), r.get('rating','').strip())
        rep_map[key] = r

rows = []
with orig.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames[:] if reader.fieldnames else []
    for r in reader:
        rows.append(r)

# Ensure output has distribution_generated flag
if 'distribution_generated' not in fieldnames:
    fieldnames.append('distribution_generated')

updated_count = 0
for r in rows:
    key = (r.get('name','').strip(), r.get('city','').strip(), r.get('rating','').strip())
    if key in rep_map:
        rep = rep_map[key]
        # copy reviews_count and distribution fields
        if 'reviews_count' in rep:
            r['reviews_count'] = rep.get('reviews_count','0')
        r[one] = rep.get(one, r.get(one,'0'))
        r[two] = rep.get(two, r.get(two,'0'))
        r[three] = rep.get(three, r.get(three,'0'))
        r[four] = rep.get(four, r.get(four,'0'))
        r[five] = rep.get(five, r.get(five,'0'))
        r['distribution_generated'] = '1'
        updated_count += 1
    else:
        # preserve existing or set flag to 0
        r['distribution_generated'] = r.get('distribution_generated','0')

with out.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f'Wrote {len(rows)} rows to {out}; updated {updated_count} rows from report ({len(rep_map)} report rows).')
