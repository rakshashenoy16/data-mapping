from src.mapper import map_data


if __name__ == "__main__":
    summary = map_data(
        "data/raw_data.csv",
        "data/reference_data.xlsx",
        "mapped_output"
    )

    print("\n===== SUMMARY REPORT =====")
    for key, value in summary.items():
        print(f"{key}: {value}")
