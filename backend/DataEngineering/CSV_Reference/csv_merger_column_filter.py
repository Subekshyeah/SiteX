#!/usr/bin/env python3

import argparse
import pandas as pd
import sys
from pathlib import Path


def build_parser():
    return argparse.ArgumentParser(
        prog="merge_csv.py",
        description="""
Merge multiple CSV files and keep only the specified columns.

The script reads one or more CSV files, extracts the requested columns,
and concatenates all rows into a single output CSV file.
Missing columns are filled with empty values.
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="""
%(prog)s file1.csv file2.csv ... -c COLUMN [COLUMN ...] -o OUTPUT.csv

Examples:
  %(prog)s users1.csv users2.csv -c id name email -o merged.csv

  %(prog)s data/*.csv -c id name email age -o all_users.csv

  %(prog)s reports/jan.csv reports/feb.csv reports/mar.csv \\
      -c customer_id amount status \\
      -o quarterly_report.csv
""",
        epilog="""
Notes:
  - At least one input CSV file is required.
  - -c / --columns is required.
  - -o / --output is required.
  - Missing columns in a CSV file will be created with empty values.
  - Input files are merged row-wise (concatenated).
"""
    )


def main():
    parser = build_parser()

    # Show help if no arguments were provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(
            "\nError: No arguments supplied.\n\n"
            "Example:\n"
            "  python merge_csv.py file1.csv file2.csv "
            "-c id name email -o merged.csv"
        )

    parser.add_argument(
        "csv_files",
        nargs="+",
        metavar="CSV",
        help="Input CSV file(s)"
    )

    parser.add_argument(
        "-c",
        "--columns",
        required=True,
        nargs="+",
        metavar="COLUMN",
        help="Columns to keep in the output"
    )

    parser.add_argument(
        "-o",
        "--output",
        required=True,
        metavar="FILE",
        help="Output CSV filename"
    )

    args = parser.parse_args()

    dataframes = []

    for csv_file in args.csv_files:
        try:
            print(f"Reading: {csv_file}")

            df = pd.read_csv(csv_file)

            missing = [
                col for col in args.columns
                if col not in df.columns
            ]

            if missing:
                print(
                    f"  Warning: Missing columns in {csv_file}: "
                    f"{', '.join(missing)}"
                )

            # Keep requested columns; create missing ones as empty
            selected_df = df.reindex(columns=args.columns)

            dataframes.append(selected_df)

        except FileNotFoundError:
            print(f"Error: File not found: {csv_file}")

        except pd.errors.EmptyDataError:
            print(f"Error: Empty CSV file: {csv_file}")

        except Exception as e:
            print(f"Error reading {csv_file}: {e}")

    if not dataframes:
        sys.exit("No valid CSV files were processed.")

    merged_df = pd.concat(dataframes, ignore_index=True)

    output_path = Path(args.output)

    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)

    merged_df.to_csv(output_path, index=False)

    print("\nMerge complete.")
    print(f"Files processed : {len(dataframes)}")
    print(f"Rows written    : {len(merged_df)}")
    print(f"Output file     : {output_path}")


if __name__ == "__main__":
    main()
