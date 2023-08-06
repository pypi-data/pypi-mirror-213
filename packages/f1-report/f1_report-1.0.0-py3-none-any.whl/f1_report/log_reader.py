import os
from datetime import datetime


def read_race_data(folder_path: str) -> tuple[dict[str, datetime], dict[str, datetime]]:
    """
    Reads the race data from the given folder path.

    Args:
        folder_path (str): The path to the folder containing the data files.

    Returns:
        tuple[dict[str, datetime], dict[str, datetime]]: A tuple of start_times and end_times dictionaries.
    """
    start_times = {}
    end_times = {}

    with open(os.path.join(folder_path, "start.log"), "r") as start_file, \
            open(os.path.join(folder_path, "end.log"), "r") as end_file:
        start_lines = start_file.readlines()
        end_lines = end_file.readlines()

        for start_line, end_line in zip(start_lines, end_lines):
            start_initials = start_line[:3]
            start_time_str = start_line[3:].strip()
            start_times[start_initials] = datetime.strptime(start_time_str, "%Y-%m-%d_%H:%M:%S.%f")

            end_initials = end_line[:3]
            end_time_str = end_line[3:].strip()
            end_times[end_initials] = datetime.strptime(end_time_str, "%Y-%m-%d_%H:%M:%S.%f")

    return start_times, end_times


def read_abbreviations(folder_path: str) -> dict[str, dict[str, str]]:
    """
    Reads the abbreviations data from the given folder path.

    Args:
        folder_path (str): The path to the folder containing the abbreviations file.

    Returns:
        dict[str, dict[str, str]]: A dictionary of abbreviations with driver names and team names.
    """
    abbreviations = {}

    with open(os.path.join(folder_path, "abbreviations.txt"), "r", encoding="utf-8") as abbrev_file:
        for line in abbrev_file:
            initials, driver_name, team_name = line.strip().split("_")
            abbreviations[initials] = {"driver": driver_name, "team": team_name}

    return abbreviations
