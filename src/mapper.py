import pandas as pd
import logging
import os
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def map_data(raw_file_path, reference_file_path, output_prefix):
    """
    Maps raw_data values with reference_data based on lookup_key.
    Generates:
    - matched output file
    - unmatched output file
    - summary report
    """

    # ---------- File Validation ----------
    if not os.path.exists(raw_file_path):
        raise FileNotFoundError(f"{raw_file_path} not found")

    if not os.path.exists(reference_file_path):
        raise FileNotFoundError(f"{reference_file_path} not found")

    # ---------- Load Data ----------
    logging.info("Loading raw data...")
    raw_df = pd.read_csv(raw_file_path)

    logging.info("Loading reference data...")
    ref_df = pd.read_excel(reference_file_path)

    # ---------- Column Validation ----------
    if "lookup_key" not in raw_df.columns:
        raise ValueError("lookup_key column missing in raw data")

    if "lookup_key" not in ref_df.columns:
        raise ValueError("lookup_key column missing in reference data")

    # ---------- Remove Duplicates ----------
    total_raw = len(raw_df)
    raw_unique = raw_df["lookup_key"].drop_duplicates()
    unique_count = len(raw_unique)

    logging.info(f"Total raw records: {total_raw}")
    logging.info(f"Unique lookup keys: {unique_count}")

    # ---------- Matching ----------
    matched_df = ref_df[ref_df["lookup_key"].isin(raw_unique)]

    # ---------- Unmatched ----------
    unmatched_keys = raw_unique[~raw_unique.isin(ref_df["lookup_key"])]
    unmatched_df = pd.DataFrame({"lookup_key": unmatched_keys})

    matched_count = len(matched_df)
    unmatched_count = len(unmatched_df)

    logging.info(f"Matched records: {matched_count}")
    logging.info(f"Unmatched records: {unmatched_count}")

    # ---------- Sort Output ----------
    if "date_added" in matched_df.columns:
        matched_df = matched_df.sort_values(by="date_added")

    # ---------- Timestamped Output ----------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    matched_file = f"{output_prefix}_{timestamp}.csv"
    unmatched_file = f"unmatched_{timestamp}.csv"

    matched_df.to_csv(matched_file, index=False)
    unmatched_df.to_csv(unmatched_file, index=False)

    # ---------- Summary ----------
    summary = {
        "total_raw_records": total_raw,
        "unique_lookup_keys": unique_count,
        "matched_records": matched_count,
        "unmatched_records": unmatched_count,
        "matched_output_file": matched_file,
        "unmatched_output_file": unmatched_file
    }

    return summary
