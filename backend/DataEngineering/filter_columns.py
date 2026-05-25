import pandas as pd
import numpy as np

# Read the CSV file with proper settings
csv_file = r'd:\projects\SiteX\backend\Data\CSV\master_cafes_metrics.csv'
print("Reading CSV file...")
df = pd.read_csv(csv_file, dtype=str, low_memory=False, na_filter=False)

print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# Get row 1334 (1-indexed, so index 1333)
print("Processing row 1334...")
row_1334 = df.iloc[1333]

# Find columns where the value in row 1334 is exactly '1'
columns_to_delete = [col for col, value in row_1334.items() if str(value).strip() == '1']

print(f"\nColumns with value '1' in row 1334: {len(columns_to_delete)}")
if columns_to_delete:
    print(f"First 20 columns to delete: {columns_to_delete[:20]}")
    
    # Delete those columns
    print("Deleting columns...")
    df_filtered = df.drop(columns=columns_to_delete)
    
    print(f"\nOriginal shape: {df.shape}")
    print(f"Filtered shape: {df_filtered.shape}")
    
    # Save the filtered dataframe to a new CSV file
    output_file = r'd:\projects\SiteX\backend\Data\CSV\master_cafes_metrics_filtered.csv'
    print(f"Saving filtered CSV to: {output_file}")
    df_filtered.to_csv(output_file, index=False)
    print("Done!")
else:
    print("No columns with value '1' found in row 1334")
