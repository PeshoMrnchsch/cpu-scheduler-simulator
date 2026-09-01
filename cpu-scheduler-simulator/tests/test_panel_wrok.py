import pytest

from src.gui.workload_panel import WorkloadPanel
from PySide6.QtCore import Qt

class TestWorkloadPanel:

    def test_initial_state(self, workload_panel):
        assert workload_panel.table.rowCount() == 0
        assert workload_panel.table.columnCount() == 3

    def test_add_empty_process(self, workload_panel):
        workload_panel.add_empty_process()

        assert workload_panel.table.rowCount() == 1
        assert workload_panel.table.item(0, 0).text() == "P1"
        assert workload_panel.table.item(0, 1).text() == ""
        assert workload_panel.table.item(0, 2).text() == ""

    def test_add_multiple_empty_processes(self, workload_panel):
        workload_panel.add_empty_process()
        workload_panel.add_empty_process()
        workload_panel.add_empty_process()

        assert workload_panel.table.rowCount() == 3
        assert workload_panel.table.item(0, 0).text() == "P1"
        assert workload_panel.table.item(1, 0).text() == "P2"
        assert workload_panel.table.item(2, 0).text() == "P3"

    def test_add_process(self, workload_panel):
        workload_panel.add_process("P1", 0, 5)

        assert workload_panel.table.rowCount() == 1
        assert workload_panel.table.item(0, 0).text() == "P1"
        assert workload_panel.table.item(0, 1).text() == "0"
        assert workload_panel.table.item(0, 2).text() == "5"

    def test_remove_process(self, workload_panel):
        workload_panel.add_process("P1", 0, 5)
        workload_panel.add_process("P2", 1, 3)

        workload_panel.table.selectRow(0)
        workload_panel.remove_process()

        assert workload_panel.table.rowCount() == 1

    def test_remove_process_without_selection(self, workload_panel):
        workload_panel.add_process("P1", 0, 5)

        workload_panel.remove_process()

        assert workload_panel.table.rowCount() == 1

    def test_convert_to_workload(self, workload_panel):
        workload_panel.add_process("P1", 0, 5)
        workload_panel.add_process("P2", 1, 3)
        workload_panel.add_process("P3", 2, 4)

        workload = workload_panel.convert_to_workload()

        assert len(workload.processes) == 3

        assert workload.processes[0].pid == "P1"
        assert workload.processes[0].arrival_time == 0
        assert workload.processes[0].burst_time == 5

        assert workload.processes[1].pid == "P2"
        assert workload.processes[1].arrival_time == 1
        assert workload.processes[1].burst_time == 3

        assert workload.processes[2].pid == "P3"
        assert workload.processes[2].arrival_time == 2
        assert workload.processes[2].burst_time == 4

    def test_empty_workload(self, workload_panel):
        with pytest.raises(ValueError, match="Workload cannot be empty"):
            workload_panel.convert_to_workload()

    def test_automatic_pids(self, workload_panel):
        workload_panel.add_empty_process()
        workload_panel.add_empty_process()
        workload_panel.add_empty_process()

        assert workload_panel.table.item(0, 0).text() == "P1"
        assert workload_panel.table.item(1, 0).text() == "P2"
        assert workload_panel.table.item(2, 0).text() == "P3"

    def test_duplicate_pid(self, workload_panel):
        workload_panel.add_process("P1", 0, 5)
        workload_panel.add_process("P1", 1, 3)

        with pytest.raises(ValueError, match="already exists"):
            workload_panel.convert_to_workload()

    def test_empty_arrival(self, workload_panel):
        workload_panel.add_empty_process()

        workload_panel.table.item(0, 0).setText("P1")
        workload_panel.table.item(0, 2).setText("5")

        with pytest.raises(ValueError, match="Arrival time cannot be empty"):
            workload_panel.convert_to_workload()

    def test_invalid_arrival(self, workload_panel):
        workload_panel.add_process("P1", "abc", 5)

        with pytest.raises(ValueError, match="Arrival time must be an integer"):
            workload_panel.convert_to_workload()

    def test_negative_arrival(self, workload_panel):
        workload_panel.add_process("P1", -1, 5)

        with pytest.raises(ValueError, match="Arrival time cannot be negative"):
            workload_panel.convert_to_workload()

    def test_empty_burst(self, workload_panel):
        workload_panel.add_empty_process()

        workload_panel.table.item(0, 0).setText("P1")
        workload_panel.table.item(0, 1).setText("0")

        with pytest.raises(ValueError, match="Burst time cannot be empty"):
            workload_panel.convert_to_workload()

    def test_invalid_burst(self, workload_panel):
        workload_panel.add_process("P1", 0, "abc")

        with pytest.raises(ValueError, match="Burst time must be an integer"):
            workload_panel.convert_to_workload()

    def test_zero_burst(self, workload_panel):
        workload_panel.add_process("P1", 0, 0)

        with pytest.raises(ValueError, match="Burst time must be greater than 0"):
            workload_panel.convert_to_workload()

    def test_negative_burst(self, workload_panel):
        workload_panel.add_process("P1", 0, -5)

        with pytest.raises(ValueError, match="Burst time must be greater than 0"):
            workload_panel.convert_to_workload()

    def test_clear(self, workload_panel):
        workload_panel.add_process("P1", 0, 5)
        workload_panel.add_process("P2", 1, 3)

        workload_panel.clear()

        assert workload_panel.table.rowCount() == 0

    def test_pid_is_not_editable(self, workload_panel):
        workload_panel.add_empty_process()

        item = workload_panel.table.item(0, 0)

        assert not (
            item.flags() & Qt.ItemFlag.ItemIsEditable
        )