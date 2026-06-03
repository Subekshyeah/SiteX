"""
Generates spatialite_migration.ipynb with per-CSV tables
using only the columns identified as significant by the GNN Column Analysis.
"""
import json
import uuid
from pathlib import Path

def make_id():
    return uuid.uuid4().hex[:8]

cells = []

def add_md(text):
    lines = text.rstrip('\n').split('\n')
    source = [line + '\n' for line in lines[:-1]] + [lines[-1]]
    cells.append({
        "cell_type": "markdown",
        "id": make_id(),
        "metadata": {},
        "source": source
    })

def add_code(text):
    lines = text.rstrip('\n').split('\n')
    source = [line + '\n' for line in lines[:-1]] + [lines[-1]]
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "id": make_id(),
        "metadata": {},
        "outputs": [],
        "source": source
    })

# ═══════════════════════════════════════════════════════════════════════
# CELL 1: Title
# ═══════════════════════════════════════════════════════════════════════
add_md("""# SiteX: CSV to SpatiaLite Migration Pipeline (GNN-Optimized)

This notebook manages the migration from independent CSV files to a unified, spatially-indexed
SQLite database (`sitex_geospatial.db`). Each CSV gets its own dedicated table with **only the
columns identified as significant** by the GNN Column Analysis.

### Architecture:
| Table | Source CSV | Rows | Columns |
|-------|-----------|------|---------|
| `cafes` | cafes.csv | 4,052 | 11 features |
| `banks` | banks_all_data.csv | 613 | 17 features |
| `temples` | temples_all_data.csv | 2,200 | 16 features |
| `health` | health_all_data.csv | 1,575 | 16 features |
| `education` | education_all_data.csv | 1,804 | 13 features |
| `other_pois` | other_all_data.csv | 1,913 | 16 features |
| `cafe_metrics` | (computed) | — | Pre-computed GNN edge features |

### Column Selection Criteria (from GNN Analysis):
- **Included**: Node identifiers, spatial coords, numerical & categorical node features
- **Excluded**: Entirely null columns (`state`, `price`), duplicate columns (`place_id`, `category`, `categoryName`, etc.), and explicitly excluded columns (`country`, `permanentlyClosed`, `hours`, `weekly_hours_norm`, etc.)

### Requirements:
```bash
pip install pandas spatialite
```""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 2: pip install
# ═══════════════════════════════════════════════════════════════════════
add_code("%pip install pandas spatialite")

# ═══════════════════════════════════════════════════════════════════════
# CELL 3: Imports + Configuration
# ═══════════════════════════════════════════════════════════════════════
add_code("""import sqlite3
import pandas as pd
import os
import sys
import platform
from pathlib import Path
from collections import OrderedDict

# Paths configuration relative to notebooks directory
WORKSPACE_DIR = Path('..')
DB_PATH = WORKSPACE_DIR / 'sitex_geospatial.db'
CSV_DIR = WORKSPACE_DIR / 'DataEngineering' / 'CSV_Reference'

# ═══════════════════════════════════════════════════════════════════════
# Table definitions derived from GNN Column Analysis
# ═══════════════════════════════════════════════════════════════════════
# Column Roles (per analysis):
#   Identifiers  -> High-cardinality TEXT columns (GNN node IDs)
#   Spatial      -> lat/lng for SpatiaLite POINT geometry + R-tree index
#   Categorical  -> Low-cardinality features (one-hot/embedding candidates)
#   Numerical    -> Continuous features for GNN node attributes
#
# Format: { csv: filename, columns: OrderedDict(db_col -> (SQL_TYPE, csv_col)) }
# ═══════════════════════════════════════════════════════════════════════

TABLE_CONFIGS = OrderedDict([
    # ── CAFES (cafes.csv | 4052 rows) ──────────────────────────────────
    # Identifiers: name, address, imageUrl
    # Numerical:   weekly_hours, rating, reviews_count, rank
    # Categorical: main_category (105 unique), city (79 unique)
    ('cafes', {
        'csv': 'cafes.csv',
        'columns': OrderedDict([
            ('name',           ('TEXT', 'name')),
            ('address',        ('TEXT', 'address')),
            ('image_url',      ('TEXT', 'imageUrl')),
            ('lat',            ('REAL NOT NULL', 'lat')),
            ('lng',            ('REAL NOT NULL', 'lng')),
            ('main_category',  ('TEXT', 'main_category')),
            ('city',           ('TEXT', 'city')),
            ('rating',         ('REAL', 'rating')),
            ('reviews_count',  ('INTEGER', 'reviews_count')),
            ('rank',           ('INTEGER', 'rank')),
            ('weekly_hours',   ('REAL', 'weekly_hours')),
        ]),
    }),

    # ── BANKS (banks_all_data.csv | 613 rows) ──────────────────────────
    # Identifiers: name, address, street, imageUrl
    # Numerical:   rating, rating_norm, reviews_count, reviews_raw, reviews_norm,
    #              rank, filled_rank, weekly_hours, weekly_hours_raw
    # Categorical: main_category (5 unique), city (24 unique)
    ('banks', {
        'csv': 'banks_all_data.csv',
        'columns': OrderedDict([
            ('name',              ('TEXT', 'name')),
            ('address',           ('TEXT', 'address')),
            ('street',            ('TEXT', 'street')),
            ('image_url',         ('TEXT', 'imageUrl')),
            ('lat',               ('REAL NOT NULL', 'lat')),
            ('lng',               ('REAL NOT NULL', 'lng')),
            ('main_category',     ('TEXT', 'main_category')),
            ('city',              ('TEXT', 'city')),
            ('rating',            ('REAL', 'rating')),
            ('rating_norm',       ('REAL', 'rating_norm')),
            ('reviews_count',     ('INTEGER', 'reviews_count')),
            ('reviews_raw',       ('REAL', 'reviews_raw')),
            ('reviews_norm',      ('REAL', 'reviews_norm')),
            ('rank',              ('INTEGER', 'rank')),
            ('filled_rank',       ('INTEGER', 'filled_rank')),
            ('weekly_hours',      ('REAL', 'weekly_hours')),
            ('weekly_hours_raw',  ('REAL', 'weekly_hours_raw')),
        ]),
    }),

    # ── TEMPLES (temples_all_data.csv | 2200 rows) ────────────────────
    # Identifiers: name, address, street, imageUrl
    # Numerical:   rating, rating_norm, reviews_count, reviews_raw, reviews_norm,
    #              rank, filled_rank, weekly_hours
    # Categorical: main_category (24 unique), city (51 unique)
    ('temples', {
        'csv': 'temples_all_data.csv',
        'columns': OrderedDict([
            ('name',              ('TEXT', 'name')),
            ('address',           ('TEXT', 'address')),
            ('street',            ('TEXT', 'street')),
            ('image_url',         ('TEXT', 'imageUrl')),
            ('lat',               ('REAL NOT NULL', 'lat')),
            ('lng',               ('REAL NOT NULL', 'lng')),
            ('main_category',     ('TEXT', 'main_category')),
            ('city',              ('TEXT', 'city')),
            ('rating',            ('REAL', 'rating')),
            ('rating_norm',       ('REAL', 'rating_norm')),
            ('reviews_count',     ('INTEGER', 'reviews_count')),
            ('reviews_raw',       ('REAL', 'reviews_raw')),
            ('reviews_norm',      ('REAL', 'reviews_norm')),
            ('rank',              ('INTEGER', 'rank')),
            ('filled_rank',       ('INTEGER', 'filled_rank')),
            ('weekly_hours',      ('REAL', 'weekly_hours')),
        ]),
    }),

    # ── HEALTH (health_all_data.csv | 1575 rows) ──────────────────────
    # Identifiers: name, address, imageUrl
    # Numerical:   rating, rating_norm, reviews_count, reviews_raw, reviews_norm,
    #              rank, filled_rank, weekly_hours, weekly_hours_raw
    # Categorical: main_category (78 unique), city (35 unique)
    ('health', {
        'csv': 'health_all_data.csv',
        'columns': OrderedDict([
            ('name',              ('TEXT', 'name')),
            ('address',           ('TEXT', 'address')),
            ('image_url',         ('TEXT', 'imageUrl')),
            ('lat',               ('REAL NOT NULL', 'lat')),
            ('lng',               ('REAL NOT NULL', 'lng')),
            ('main_category',     ('TEXT', 'main_category')),
            ('city',              ('TEXT', 'city')),
            ('rating',            ('REAL', 'rating')),
            ('rating_norm',       ('REAL', 'rating_norm')),
            ('reviews_count',     ('INTEGER', 'reviews_count')),
            ('reviews_raw',       ('REAL', 'reviews_raw')),
            ('reviews_norm',      ('REAL', 'reviews_norm')),
            ('rank',              ('INTEGER', 'rank')),
            ('filled_rank',       ('INTEGER', 'filled_rank')),
            ('weekly_hours',      ('REAL', 'weekly_hours')),
            ('weekly_hours_raw',  ('REAL', 'weekly_hours_raw')),
        ]),
    }),

    # ── EDUCATION (education_all_data.csv | 1804 rows) ────────────────
    # Identifiers: name, address, imageUrl
    # Numerical:   rating, rating_norm, rank, filled_rank,
    #              weekly_hours, weekly_hours_raw
    # Categorical: main_category (80 unique), city (46 unique)
    # NOTE: No reviews columns — analysis did not flag them as significant
    ('education', {
        'csv': 'education_all_data.csv',
        'columns': OrderedDict([
            ('name',              ('TEXT', 'name')),
            ('address',           ('TEXT', 'address')),
            ('image_url',         ('TEXT', 'imageUrl')),
            ('lat',               ('REAL NOT NULL', 'lat')),
            ('lng',               ('REAL NOT NULL', 'lng')),
            ('main_category',     ('TEXT', 'main_category')),
            ('city',              ('TEXT', 'city')),
            ('rating',            ('REAL', 'rating')),
            ('rating_norm',       ('REAL', 'rating_norm')),
            ('rank',              ('INTEGER', 'rank')),
            ('filled_rank',       ('INTEGER', 'filled_rank')),
            ('weekly_hours',      ('REAL', 'weekly_hours')),
            ('weekly_hours_raw',  ('REAL', 'weekly_hours_raw')),
        ]),
    }),

    # ── OTHER POIs (other_all_data.csv | 1913 rows) ───────────────────
    # Identifiers: name, address, imageUrl
    # Numerical:   rating, rating_norm, reviews_count, reviews_raw, reviews_norm,
    #              rank, filled_rank, weekly_hours, weekly_hours_raw
    # Categorical: main_category (191 unique), city (47 unique)
    ('other_pois', {
        'csv': 'other_all_data.csv',
        'columns': OrderedDict([
            ('name',              ('TEXT', 'name')),
            ('address',           ('TEXT', 'address')),
            ('image_url',         ('TEXT', 'imageUrl')),
            ('lat',               ('REAL NOT NULL', 'lat')),
            ('lng',               ('REAL NOT NULL', 'lng')),
            ('main_category',     ('TEXT', 'main_category')),
            ('city',              ('TEXT', 'city')),
            ('rating',            ('REAL', 'rating')),
            ('rating_norm',       ('REAL', 'rating_norm')),
            ('reviews_count',     ('INTEGER', 'reviews_count')),
            ('reviews_raw',       ('REAL', 'reviews_raw')),
            ('reviews_norm',      ('REAL', 'reviews_norm')),
            ('rank',              ('INTEGER', 'rank')),
            ('filled_rank',       ('INTEGER', 'filled_rank')),
            ('weekly_hours',      ('REAL', 'weekly_hours')),
            ('weekly_hours_raw',  ('REAL', 'weekly_hours_raw')),
        ]),
    }),
])

print(f"Python executable: {sys.executable}")
print(f"Database: {DB_PATH.resolve()}")
print(f"CSV source: {CSV_DIR.resolve()}")
print(f"Tables to create: {list(TABLE_CONFIGS.keys())}")
print(f"64-bit Python: {sys.maxsize > 2**32}")""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 4: Markdown - DB Init
# ═══════════════════════════════════════════════════════════════════════
add_md("""## 1. Database Initialization
Create an empty database and enable the SpatiaLite extension which provides functions like `ST_Distance` and R-tree clustering indexing.""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 5: DB Init Code
# ═══════════════════════════════════════════════════════════════════════
add_code("""# Start fresh
if DB_PATH.exists():
    try:
        os.remove(DB_PATH)
        print("Removed existing database for a clean start.")
    except PermissionError:
        print("Database is currently locked. Ensure no other applications are using it.")

# Establish connection
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Platform-specific setup for SpatiaLite
is_windows = platform.system() == 'Windows'
is_linux = platform.system() == 'Linux'

if is_windows:
    spatialite_dir = WORKSPACE_DIR / 'mod_spatialite-5.1.0-win-amd64'
    if spatialite_dir.exists():
        os.environ['PATH'] = str(spatialite_dir.resolve()) + ';' + os.environ.get('PATH', '')
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(str(spatialite_dir.resolve()))
        print(f"Added local SpatiaLite directory to PATH: {spatialite_dir}")
    else:
        print(f"SpatiaLite directory not found at {spatialite_dir}, will try system installation.")
elif is_linux:
    print("Linux detected - using system-installed SpatiaLite")

# Enable spatial capabilities
conn.enable_load_extension(True)
try:
    conn.load_extension('mod_spatialite')
    print("SpatiaLite extension enabled.")
except Exception as e:
    print(f"Error loading SpatiaLite: {e}")
    if is_linux:
        print("  On Linux, install SpatiaLite with: sudo apt-get install libspatialite-dev")
    raise e
conn.enable_load_extension(False)

# Initialize standard spatial metadata
cursor.execute("SELECT InitSpatialMetaData(1)")
conn.commit()
print("Spatial metadata initialized.")""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 6: Markdown - Schema
# ═══════════════════════════════════════════════════════════════════════
add_md("""## 2. Schema Definition (Per-CSV Tables with Spatial Geometry)

Creates one table per CSV source file. Each table includes:
- Only the GNN-significant columns identified by the analysis
- An auto-increment `id` primary key
- A SpatiaLite `POINT` geometry column (EPSG 4326 = WGS84 GPS)
- An R-tree spatial index for fast radius/proximity queries

Additionally creates `cafe_metrics` for pre-computed GNN edge features.""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 7: Schema Creation Code
# ═══════════════════════════════════════════════════════════════════════
add_code("""print("Building tables from GNN analysis config...\\n")

# Drop all existing tables
for table_name in list(TABLE_CONFIGS.keys()) + ['cafe_metrics']:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

# Create each table dynamically from TABLE_CONFIGS
for table_name, config in TABLE_CONFIGS.items():
    col_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
    for col_name, (sql_type, _csv_col) in config['columns'].items():
        col_defs.append(f"{col_name} {sql_type}")

    create_sql = f"CREATE TABLE {table_name} (\\n    " + ",\\n    ".join(col_defs) + "\\n)"
    cursor.execute(create_sql)

    # Add SpatiaLite geometry column + R-tree spatial index
    cursor.execute(f"SELECT AddGeometryColumn('{table_name}', 'geometry', 4326, 'POINT', 'XY')")
    cursor.execute(f"SELECT CreateSpatialIndex('{table_name}', 'geometry')")

    n_cols = len(config['columns'])
    print(f"  {table_name:<15} | {n_cols:>2} columns + geometry | source: {config['csv']}")

# Pre-computed GNN edge connection metrics (cafe-centric)
cursor.execute(\"\"\"
    CREATE TABLE cafe_metrics (
        cafe_id INTEGER PRIMARY KEY,
        nearest_bank_dist REAL,
        nearest_school_dist REAL,
        nearest_temple_dist REAL,
        nearest_health_dist REAL,
        poi_count_500m INTEGER,
        road_network_node_id INTEGER,
        FOREIGN KEY(cafe_id) REFERENCES cafes(id)
    )
\"\"\")
print(f"  {'cafe_metrics':<15} | Pre-computed edge features")

conn.commit()
print("\\nSchema definitions successful and geometry columns created!")""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 8: Markdown - ETL
# ═══════════════════════════════════════════════════════════════════════
add_md("""## 3. Extract & Load Process

Generic ETL loader that:
1. Reads each CSV file
2. Extracts only the columns defined in `TABLE_CONFIGS`
3. Handles type conversion (TEXT, REAL, INTEGER) with null-safety
4. Generates SpatiaLite `POINT()` geometry from lat/lng coordinates""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 9: ETL Code
# ═══════════════════════════════════════════════════════════════════════
add_code("""def load_csv_to_table(table_name, config):
    \"\"\"Generic loader: CSV -> SpatiaLite table using column config.\"\"\"
    csv_path = CSV_DIR / config['csv']
    if not csv_path.exists():
        print(f"  SKIP {table_name}: {config['csv']} not found at {csv_path}")
        return 0

    df = pd.read_csv(csv_path)
    columns = config['columns']
    db_cols = list(columns.keys())

    placeholders = ', '.join(['?'] * len(db_cols))
    insert_sql = f"INSERT INTO {table_name} ({', '.join(db_cols)}) VALUES ({placeholders})"

    count = 0
    for _, row in df.iterrows():
        values = []
        lat_val = lng_val = None

        for db_col, (sql_type, csv_col) in columns.items():
            raw = row.get(csv_col)

            # Null handling
            if pd.isna(raw) or raw == '' or str(raw).strip() == 'nan':
                values.append(None)
            elif 'INTEGER' in sql_type:
                try:
                    values.append(int(float(raw)))
                except (ValueError, TypeError):
                    values.append(None)
            elif 'REAL' in sql_type:
                try:
                    values.append(float(raw))
                except (ValueError, TypeError):
                    values.append(None)
            else:
                values.append(str(raw))

            # Track spatial coords for geometry generation
            if db_col == 'lat':
                lat_val = values[-1]
            elif db_col == 'lng':
                lng_val = values[-1]

        cursor.execute(insert_sql, values)
        last_id = cursor.lastrowid

        # Generate SpatiaLite POINT geometry
        if lat_val is not None and lng_val is not None:
            cursor.execute(
                f"UPDATE {table_name} SET geometry = GeomFromText('POINT({lng_val} {lat_val})', 4326) WHERE id = {last_id}"
            )
        count += 1

    conn.commit()
    return count


# ── Run Migration ─────────────────────────────────────────────────────
print("Migration in progress...\\n")

total = 0
for table_name, config in TABLE_CONFIGS.items():
    count = load_csv_to_table(table_name, config)
    if count > 0:
        print(f"  Loaded {count:>5} rows from {config['csv']:<30} -> `{table_name}`")
    total += count

print(f"\\nMigration completed. Total rows: {total}")""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 10: Markdown - Verification
# ═══════════════════════════════════════════════════════════════════════
add_md("""## 4. Verification & Spatial Index Test

Verify row counts across all tables and run a real-world 500m radius query using
SpatiaLite's `ST_Distance` to confirm R-tree spatial index functionality.""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 11: Verification Code
# ═══════════════════════════════════════════════════════════════════════
add_code("""print("=" * 60)
print("DATABASE STATISTICS")
print("=" * 60)

for table_name in TABLE_CONFIGS.keys():
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]

    # Get column count (excluding id and geometry)
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cursor.fetchall() if row[1] not in ('id', 'geometry')]
    print(f"  {table_name:<15} | {count:>5} rows | {len(cols):>2} feature columns")

print()

# ── Schema Inspection ──────────────────────────────────────────────────
print("=" * 60)
print("COLUMN DETAILS PER TABLE")
print("=" * 60)

for table_name in TABLE_CONFIGS.keys():
    cursor.execute(f"PRAGMA table_info({table_name})")
    cols = cursor.fetchall()
    col_names = [c[1] for c in cols if c[1] not in ('id', 'geometry')]
    print(f"\\n  {table_name}: {', '.join(col_names)}")

print()

# ── Spatial Index Test ─────────────────────────────────────────────────
print("=" * 60)
print("SPATIAL INDEX TEST (500m radius from first cafe)")
print("=" * 60)

cursor.execute("SELECT id, name FROM cafes LIMIT 1")
cafe = cursor.fetchone()

if cafe:
    print(f"\\n  Anchor: Cafe #{cafe[0]} '{cafe[1]}'")
    print()

    # Query each POI table for proximity counts
    poi_tables = ['banks', 'temples', 'health', 'education', 'other_pois']
    for poi_table in poi_tables:
        cursor.execute(f\"\"\"
            SELECT COUNT(*) 
            FROM {poi_table} 
            WHERE ST_Distance(geometry, (SELECT geometry FROM cafes WHERE id = ?), 1) < 500
        \"\"\", (cafe[0],))
        nearby = cursor.fetchone()[0]
        if nearby > 0:
            print(f"    {nearby:>3} {poi_table} within 500m")

    # Also check nearby cafes
    cursor.execute(\"\"\"
        SELECT COUNT(*) 
        FROM cafes 
        WHERE id != ? AND ST_Distance(geometry, (SELECT geometry FROM cafes WHERE id = ?), 1) < 500
    \"\"\", (cafe[0], cafe[0]))
    nearby_cafes = cursor.fetchone()[0]
    print(f"    {nearby_cafes:>3} other cafes within 500m")
else:
    print("  No cafes found to run spatial test.")

print()

# ── Sample Data ────────────────────────────────────────────────────────
print("=" * 60)
print("SAMPLE DATA (first 3 rows per table)")
print("=" * 60)

for table_name in TABLE_CONFIGS.keys():
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
    rows = cursor.fetchall()

    cursor.execute(f"PRAGMA table_info({table_name})")
    col_names = [c[1] for c in cursor.fetchall()]

    print(f"\\n  --- {table_name} ---")
    for row in rows:
        # Show id, name, lat, lng, rating, rank (key fields)
        row_dict = dict(zip(col_names, row))
        name = row_dict.get('name', 'N/A')
        lat = row_dict.get('lat', 'N/A')
        lng = row_dict.get('lng', 'N/A')
        rating = row_dict.get('rating', 'N/A')
        rank_val = row_dict.get('rank', 'N/A')
        print(f"    id={row_dict['id']} | {name[:40]:<40} | ({lat}, {lng}) | rating={rating} | rank={rank_val}")""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 12: Markdown - Cleanup
# ═══════════════════════════════════════════════════════════════════════
add_md("""## 5. Cleanup
Close the database connection. Re-run from Section 1 for a fresh migration.""")

# ═══════════════════════════════════════════════════════════════════════
# CELL 13: Close connection
# ═══════════════════════════════════════════════════════════════════════
add_code("""conn.close()
print(f"Database closed. File: {DB_PATH.resolve()}")
print(f"Database size: {DB_PATH.stat().st_size / (1024*1024):.2f} MB")""")

# ═══════════════════════════════════════════════════════════════════════
# Build notebook
# ═══════════════════════════════════════════════════════════════════════
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": ".venv",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbformat_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.14.5"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

output_path = Path(__file__).parent / 'spatialite_migration.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f"Notebook generated at: {output_path}")
print(f"  {len(cells)} cells ({sum(1 for c in cells if c['cell_type'] == 'code')} code, {sum(1 for c in cells if c['cell_type'] == 'markdown')} markdown)")
