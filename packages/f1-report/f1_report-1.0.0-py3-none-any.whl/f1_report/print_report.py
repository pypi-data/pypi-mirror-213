def print_report(best_laps: list[tuple[str, str, str]], invalid_laps: list[tuple[str, str]]) -> None:
    """
    Prints the report of best laps and invalid laps.

    Args:
        best_laps (list[tuple[str, str, str]]): List of tuples containing driver name, team name, and lap time.
        invalid_laps (list[tuple[str, str]]): List of tuples containing driver name and team name of invalid laps.
    """
    print("{:<3}  {:<20}  {:<30}  {:<10}".format("Pos.", "Driver", "Team", "Lap Time"))
    print("-" * 80)
    for i, (driver, team, lap_time) in enumerate(best_laps[:15], 1):
        print("{:<3} | {:<20} | {:<30} | {:<10}".format(f"{i}.", driver, team, lap_time))

    print("\n" + "-" * 80)
    print("Invalid Data:")
    for invalid_data in invalid_laps:
        print("{:<20} | {}".format(*invalid_data))
