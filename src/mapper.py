import pandas as pd


def map_data(raw_file_path, reference_file_path, output_file_path):
    """
    Maps raw_data values with reference_data based on lookup_key
    and saves matched rows into output file.
    """

    # Load files
    raw_df = pd.read_csv(raw_file_path)
    ref_df = pd.read_excel(reference_file_path)

    # Remove duplicates in raw data
    raw_unique = raw_df.drop_duplicates()

    # Perform matching
    mapped_df = ref_df[ref_df["lookup_key"].isin(raw_unique.iloc[:, 0])]

    # Remove duplicates in output (safety)
    mapped_df = mapped_df.drop_duplicates()

    # Save output
    mapped_df.to_csv(output_file_path, index=False)

    return mapped_df
