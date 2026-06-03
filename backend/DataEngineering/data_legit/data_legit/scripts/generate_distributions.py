#!/usr/bin/env python3
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

in_path = Path('comp/csv/compact_summary.csv')
out_path = Path('comp/csv/compact_summary_generated.csv')
report_path = Path('comp/csv/generated_report.csv')

one='reviewsDistribution_oneStar'
two='reviewsDistribution_twoStar'
three='reviewsDistribution_threeStar'
four='reviewsDistribution_fourStar'
five='reviewsDistribution_fiveStar'

def to_int(val):
    try:
        return int(float(val))
    except:
        return 0

rows = []
with in_path.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames[:] if reader.fieldnames else []
    for r in reader:
        rows.append(r)

# Collect valid reviews_count for computing medians (only rows with non-zero distribution that sums to rc)
rcs_by_rating = defaultdict(list)
all_rcs = []
for r in rows:
    rating_raw = r.get('rating','')
    try:
        rating = float(rating_raw)
    except:
        rating = 0.0
    rc = to_int(r.get('reviews_count',0))
    dsum = sum(to_int(r.get(c,0)) for c in (one,two,three,four,five))
    if rc>0 and dsum==rc:
        key = int(round(rating))
        rcs_by_rating[key].append(rc)
        all_rcs.append(rc)

# compute median fallback
if all_rcs:
    overall_med = int(statistics.median(all_rcs))
else:
    overall_med = 3
# medians per rounded rating
median_by_rating = {k:int(statistics.median(v)) for k,v in rcs_by_rating.items()}

updated = []
updated_count = 0
for r in rows:
    rating_raw = r.get('rating','')
    try:
        rating = float(rating_raw)
    except:
        rating = 0.0
    rc = to_int(r.get('reviews_count',0))
    dist = [to_int(r.get(c,0)) for c in (one,two,three,four,five)]
    dsum = sum(dist)
    changed = False

    # identify problematic cases: rc <=0 with no distribution, or dsum != rc
    if (rc <= 0 and dsum == 0 and rating > 0) or (rc > 0 and dsum != rc) or (rc <=0 and dsum>0):
        # Determine a reviews_count if needed
        if rc <= 0:
            key = int(round(rating))
            rc = median_by_rating.get(key, overall_med)
            if rc <= 0:
                rc = overall_med if overall_med>0 else 3
            r['reviews_count'] = str(rc)
            changed = True

        # if rating <= 0, we cannot sensibly create distribution; leave zeroes
        if rating <= 0:
            # set distribution to zeros and mark generated only for rc
            for c in (one,two,three,four,five):
                r[c] = '0'
            changed = True
        else:
            # generate distribution using Gaussian-like weights around rating
            k = 0.9
            weights = [math.exp(-k*((rating - s)**2)) for s in range(1,6)]
            total_w = sum(weights)
            probs = [w/total_w for w in weights]
            # raw counts
            raw = [p*rc for p in probs]
            floored = [math.floor(x) for x in raw]
            assigned = sum(floored)
            remaining = rc - assigned
            # sort by fractional part descending
            fracs = [(i, raw[i]-floored[i]) for i in range(5)]
            fracs.sort(key=lambda x: -x[1])
            final = floored[:]
            i=0
            while remaining>0:
                final[fracs[i%5][0]] += 1
                remaining -= 1
                i+=1
            # ensure non-negative
            final = [max(0,int(x)) for x in final]
            # final adjustment in case of rounding issues
            diff = rc - sum(final)
            if diff>0:
                for idx in range(5):
                    if diff==0: break
                    final[idx]+=1
                    diff-=1
            elif diff<0:
                # remove from largest
                for idx in sorted(range(5), key=lambda j: -final[j]):
                    if diff==0: break
                    take = min(final[idx], -diff)
                    final[idx]-=take
                    diff += take
            # write back
            r[one]=str(final[0])
            r[two]=str(final[1])
            r[three]=str(final[2])
            r[four]=str(final[3])
            r[five]=str(final[4])
            changed = True

    # If distribution present and correct, keep unchanged
    if changed:
        updated.append({
            'name': r.get('name',''),
            'city': r.get('city',''),
            'rating': r.get('rating',''),
            'reviews_count': r.get('reviews_count','0'),
            one: r.get(one,'0'),
            two: r.get(two,'0'),
            three: r.get(three,'0'),
            four: r.get(four,'0'),
            five: r.get(five,'0'),
        })
        updated_count += 1

# Write new CSV (preserve original columns and append `distribution_generated` flag)
new_fieldnames = fieldnames[:] if fieldnames else []
if 'distribution_generated' not in new_fieldnames:
    new_fieldnames.append('distribution_generated')

with out_path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=new_fieldnames)
    writer.writeheader()
    for r in rows:
        # add flag
        name = r.get('name','')
        # determine if this row is in updated list (cheap check via comparison)
        flag = '1' if any(u['name']==name and u.get('rating','')==r.get('rating','') for u in updated) else '0'
        r['distribution_generated'] = flag
        writer.writerow(r)

# Write a small report CSV with updated rows
rep_fields = ['name','city','rating','reviews_count',one,two,three,four,five]
with report_path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rep_fields)
    writer.writeheader()
    for u in updated:
        writer.writerow(u)

print(f'Processed {len(rows)} rows; updated {updated_count} rows.')
print(f'Generated file: {out_path}\nReport: {report_path}')
