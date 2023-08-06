from datetime import datetime


def build_report(start_times: dict[str, datetime], end_times: dict[str, datetime],
                 abbreviations: dict[str, dict[str, str]]) -> tuple[list[tuple[str, str, str]], list[tuple[str, str]]]:
    """
    Builds the report of best laps and invalid laps based on the start times, end times, and abbreviations.

    Args:
        start_times (dict[str, datetime]): A dictionary of start times for each driver.
        end_times (dict[str, datetime]): A dictionary of end times for each driver.
        abbreviations (dict[str, dict[str, str]]): A dictionary of abbreviations with driver names and team names.

    Returns:
        tuple[list[tuple[str, str, str]], list[tuple[str, str]]]: A tuple of best_laps and invalid_laps lists.
    """
    best_laps = []
    invalid_laps = []

    for initials, start_time in start_times.items():
        if initials in end_times:
            end_time = end_times[initials]
            if start_time < end_time:
                lap_time = end_time - start_time
                minutes = lap_time.seconds // 60
                seconds = lap_time.seconds % 60
                milliseconds = lap_time.microseconds // 1000
                lap_time_str = f"{minutes}:{seconds:02d}.{milliseconds:03d}"

                driver_name = abbreviations.get(initials, {}).get("driver", "Unknown")
                team_name = abbreviations.get(initials, {}).get("team", "Unknown")

                best_laps.append((driver_name, team_name, lap_time_str))
            else:
                driver_name = abbreviations.get(initials, {}).get("driver", "Unknown")
                team_name = abbreviations.get(initials, {}).get("team", "Unknown")

                invalid_laps.append((driver_name, team_name))

    best_laps.sort(key=lambda x: x[2])

    return best_laps, invalid_laps
