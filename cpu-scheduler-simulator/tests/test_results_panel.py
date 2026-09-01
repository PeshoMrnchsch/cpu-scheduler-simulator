import sys

from PySide6.QtWidgets import QApplication

from src.gui.results_panel import ResultsPanel


app = QApplication.instance()

if app is None:
    app = QApplication(sys.argv)


class TestResultsPanel:

    def test_three_algorithms_create_three_rows(self):
        panel = ResultsPanel()

        comparisons = {
            "FCFS": {
                "metrics": {
                    "average_waiting_time": 3.25,
                    "average_turnaround_time": 7.50,
                    "cpu_utilization": 85.0,
                }
            },
            "SJF": {
                "metrics": {
                    "average_waiting_time": 2.00,
                    "average_turnaround_time": 6.25,
                    "cpu_utilization": 90.0,
                }
            },
            "SRTF": {
                "metrics": {
                    "average_waiting_time": 1.50,
                    "average_turnaround_time": 5.75,
                    "cpu_utilization": 95.0,
                }
            },
        }

        panel.display_results(comparisons)

        # Three algorithms should create three rows
        assert panel.table.rowCount() == 3

    def test_results_table_has_at_most_four_rows(self):
        panel = ResultsPanel()
        metrics = {
            "average_waiting_time": 1.0,
            "average_turnaround_time": 2.0,
            "cpu_utilization": 90.0,
        }
        comparisons = {
            algorithm: {"metrics": metrics}
            for algorithm in ["FCFS", "SJF", "SRTF", "Round Robin", "Extra"]
        }

        panel.display_results(comparisons)

        assert panel.table.rowCount() == 4
        assert panel.table.item(3, 0).text() == "Round Robin"

    def test_result_values_are_displayed_correctly(self):
        panel = ResultsPanel()

        comparisons = {
            "FCFS": {
                "metrics": {
                    "average_waiting_time": 3.25,
                    "average_turnaround_time": 7.50,
                    "cpu_utilization": 85.0,
                }
            },
            "SJF": {
                "metrics": {
                    "average_waiting_time": 2.00,
                    "average_turnaround_time": 6.25,
                    "cpu_utilization": 90.0,
                }
            },
            "SRTF": {
                "metrics": {
                    "average_waiting_time": 1.50,
                    "average_turnaround_time": 5.75,
                    "cpu_utilization": 95.0,
                }
            },
        }

        panel.display_results(comparisons)

        # FCFS
        assert panel.table.item(0, 0).text() == "FCFS"
        assert panel.table.item(0, 1).text() == "3.25"
        assert panel.table.item(0, 2).text() == "7.50"
        assert panel.table.item(0, 3).text() == "85.00%"

        # SJF
        assert panel.table.item(1, 0).text() == "SJF"
        assert panel.table.item(1, 1).text() == "2.00"
        assert panel.table.item(1, 2).text() == "6.25"
        assert panel.table.item(1, 3).text() == "90.00%"

        # SRTF
        assert panel.table.item(2, 0).text() == "SRTF"
        assert panel.table.item(2, 1).text() == "1.50"
        assert panel.table.item(2, 2).text() == "5.75"
        assert panel.table.item(2, 3).text() == "95.00%"

    def test_column_headers_are_correct(self):
        panel = ResultsPanel()

        assert panel.table.columnCount() == 4

        assert panel.table.horizontalHeaderItem(0).text() == "Algorithm"
        assert panel.table.horizontalHeaderItem(1).text() == "Avg Waiting Time"
        assert panel.table.horizontalHeaderItem(2).text() == "Avg Turnaround Time"
        assert panel.table.horizontalHeaderItem(3).text() == "CPU Utilization"

    def test_clear_removes_results(self):
        panel = ResultsPanel()

        comparisons = {
            "FCFS": {
                "metrics": {
                    "average_waiting_time": 3.25,
                    "average_turnaround_time": 7.50,
                    "cpu_utilization": 85.0,
                }
            },
            "SJF": {
                "metrics": {
                    "average_waiting_time": 2.00,
                    "average_turnaround_time": 6.25,
                    "cpu_utilization": 90.0,
                }
            },
            "SRTF": {
                "metrics": {
                    "average_waiting_time": 1.50,
                    "average_turnaround_time": 5.75,
                    "cpu_utilization": 95.0,
                }
            },
        }

        panel.display_results(comparisons)

        assert panel.table.rowCount() == 3

        panel.clear()

        assert panel.table.rowCount() == 0

        # The table structure should remain
        assert panel.table.columnCount() == 4