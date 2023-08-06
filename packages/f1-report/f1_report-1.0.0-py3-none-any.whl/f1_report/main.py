from log_reader import read_race_data, read_abbreviations
from report_builder import build_report
from print_report import print_report


def main() -> None:
    folder_path: str = "data"

    start_times, end_times = read_race_data(folder_path)
    abbreviations = read_abbreviations(folder_path)

    best_laps, invalid_laps = build_report(start_times, end_times, abbreviations)

    print_report(best_laps, invalid_laps)


if __name__ == "__main__":
    main()

