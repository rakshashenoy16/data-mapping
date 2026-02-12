from src.mapper import map_data


if __name__ == "__main__":
    raw_file = "data/raw_data.csv"
    reference_file = "data/reference_data.xlsx"
    output_file = "mapped_output.csv"

    result = map_data(raw_file, reference_file, output_file)

    print("Mapping completed successfully!")
    print(f"Number of matched rows: {len(result)}")
