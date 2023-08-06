import unittest
from datetime import datetime
from unittest import mock
from io import StringIO

from f1_report.log_reader import read_race_data, read_abbreviations
from f1_report.report_builder import build_report
from f1_report.print_report import print_report


class TestF1Report(unittest.TestCase):

    def setUp(self):
        self.folder_path = "data"
        self.start_data = [
            "DRR2018-05-26_15:10:25.123",
            "SVF2018-05-26_15:12:35.456",
            "VB32018-05-26_15:13:45.789"
        ]
        self.end_data = [
            "DRR2018-05-26_15:12:25.123",
            "SVF2018-05-26_15:14:35.456",
            "VB32018-05-26_15:15:45.789"
        ]
        self.abbreviations_data = [
            "DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER",
            "SVF_Sebastian Vettel_FERRARI",
            "VB3_Valtteri Bottas_MERCEDES"
        ]

    def test_read_race_data(self):
        with mock.patch("builtins.open") as mock_open:
            mock_open.side_effect = [
                mock.mock_open(read_data="\n".join(self.start_data)).return_value,
                mock.mock_open(read_data="\n".join(self.end_data)).return_value
            ]
            start_times, end_times = read_race_data(self.folder_path)
            self.assertEqual(len(start_times), 3)
            self.assertEqual(len(end_times), 3)
            self.assertEqual(start_times["DRR"], datetime(2018, 5, 26, 15, 10, 25, 123000))
            self.assertEqual(end_times["DRR"], datetime(2018, 5, 26, 15, 12, 25, 123000))

    def test_read_abbreviations(self):
        with mock.patch("builtins.open") as mock_open:
            mock_open.return_value = mock.mock_open(read_data="\n".join(self.abbreviations_data)).return_value
            abbreviations = read_abbreviations(self.folder_path)
            self.assertEqual(len(abbreviations), 3)
            self.assertEqual(abbreviations["DRR"]["driver"], "Daniel Ricciardo")
            self.assertEqual(abbreviations["DRR"]["team"], "RED BULL RACING TAG HEUER")

    def test_build_report(self):
        start_times = {
            "DRR": datetime(2018, 5, 26, 15, 10, 25, 123000),
            "SVF": datetime(2018, 5, 26, 15, 12, 35, 456000),
            "VB3": datetime(2018, 5, 26, 15, 13, 45, 789000)
        }
        end_times = {
            "DRR": datetime(2018, 5, 26, 15, 12, 25, 123000),
            "SVF": datetime(2018, 5, 26, 15, 14, 35, 456000),
            "VB3": datetime(2018, 5, 26, 15, 15, 45, 789000)
        }
        abbreviations = {
            "DRR": {"driver": "Daniel Ricciardo", "team": "RED BULL RACING TAG HEUER"},
            "SVF": {"driver": "Sebastian Vettel", "team": "FERRARI"},
            "VB3": {"driver": "Valtteri Bottas", "team": "MERCEDES"}
        }
        expected_best_laps = [
            ("Daniel Ricciardo", "RED BULL RACING TAG HEUER", "2:00.000"),
            ("Sebastian Vettel", "FERRARI", "2:00.000"),
            ("Valtteri Bottas", "MERCEDES", "2:00.000")
        ]
        expected_invalid_laps = []

        best_laps, invalid_laps = build_report(start_times, end_times, abbreviations)
        self.assertEqual(best_laps, expected_best_laps)
        self.assertEqual(invalid_laps, expected_invalid_laps)

    def test_print_report(self):
        best_laps = [
            ("Daniel Ricciardo", "RED BULL RACING TAG HEUER", "2:00.000"),
            ("Sebastian Vettel", "FERRARI", "2:00.000"),
            ("Valtteri Bottas", "MERCEDES", "2:00.000")
        ]
        invalid_laps = []

        expected_output = (
            'Pos.  Driver                Team                            Lap Time  \n'
            '--------------------------------------------------------------------------------\n'
            '1.  | Daniel Ricciardo     | RED BULL RACING TAG HEUER      | 2:00.000  \n'
            '2.  | Sebastian Vettel     | FERRARI                        | 2:00.000  \n'
            '3.  | Valtteri Bottas      | MERCEDES                       | 2:00.000  \n'
            '\n'
            '--------------------------------------------------------------------------------\n'
            'Invalid Data:\n'
        )

        with mock.patch("sys.stdout", new=StringIO()) as mock_stdout:
            print_report(best_laps, invalid_laps)
            self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
