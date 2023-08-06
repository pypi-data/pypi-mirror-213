import argparse
from f1_report.log_reader import read_race_data, read_abbreviations
from f1_report.report_builder import build_report
from f1_report.print_report import print_report


def create_parser():
    parser = argparse.ArgumentParser(description="Formula 1 Race Report CLI")
    parser.add_argument("--files", required=True, help="Path to the race data files")
    parser.add_argument("--driver", help="Driver name to filter the report")
    parser.add_argument("--asc", action="store_true", help="Sort laps in ascending order")
    parser.add_argument("--desc", action="store_true", help="Sort laps in descending order")
    return parser


def filter_laps_by_driver(laps, driver_name):
    if driver_name:
        return [lap for lap in laps if lap[0].lower() == driver_name.lower()]
    return laps


def main():
    parser = create_parser()
    args = parser.parse_args()

    folder_path = args.files
    driver_name = args.driver

    start_times, end_times = read_race_data(folder_path)
    abbreviations = read_abbreviations(folder_path)

    best_laps, invalid_laps = build_report(start_times, end_times, abbreviations)

    filtered_laps = filter_laps_by_driver(best_laps, driver_name)

    if args.asc:
        filtered_laps.sort(key=lambda x: x[2])
    elif args.desc:
        filtered_laps.sort(key=lambda x: x[2], reverse=True)

    print_report(filtered_laps, invalid_laps)


if __name__ == "__main__":
    main()
