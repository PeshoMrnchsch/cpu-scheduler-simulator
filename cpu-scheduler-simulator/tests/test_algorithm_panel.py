import pytest

from src.gui.algorithm_panel import Algorithm_Panel
from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.scheduler_algorithms.SJF import SJF_Scheduler
from src.scheduler_algorithms.SRTF import SRTF_Scheduler
from src.scheduler_algorithms.RoundRobin import RoundRobin_Scheduler


class TestAlgorithmPanel:

    def test_initial_state(self, algorithm_panel):
        assert not algorithm_panel.fcfs_checkbox.isChecked()
        assert not algorithm_panel.sjf_checkbox.isChecked()
        assert not algorithm_panel.srtf_checkbox.isChecked()
        assert not algorithm_panel.rr_checkbox.isChecked()

        assert algorithm_panel.quantum_input.value() == 2
        assert not algorithm_panel.quantum_input.isEnabled()
        assert not algorithm_panel.quantum_label.isEnabled()

    def test_round_robin_options_enabled(self, algorithm_panel):
        algorithm_panel.rr_checkbox.setChecked(True)

        assert algorithm_panel.quantum_input.isEnabled()
        assert algorithm_panel.quantum_label.isEnabled()

    def test_round_robin_options_disabled(self, algorithm_panel):
        algorithm_panel.rr_checkbox.setChecked(True)
        algorithm_panel.rr_checkbox.setChecked(False)

        assert not algorithm_panel.quantum_input.isEnabled()
        assert not algorithm_panel.quantum_label.isEnabled()

    def test_no_algorithm_selected(self, algorithm_panel):
        with pytest.raises(
            ValueError,
            match="At least one algorithm must be selected"
        ):
            algorithm_panel.get_algorithms()

    def test_fcfs_selected(self, algorithm_panel):
        algorithm_panel.fcfs_checkbox.setChecked(True)

        algorithms = algorithm_panel.get_algorithms()

        assert len(algorithms) == 1
        assert isinstance(algorithms[0], FCFS_Scheduler)

    def test_sjf_selected(self, algorithm_panel):
        algorithm_panel.sjf_checkbox.setChecked(True)

        algorithms = algorithm_panel.get_algorithms()

        assert len(algorithms) == 1
        assert isinstance(algorithms[0], SJF_Scheduler)

    def test_srtf_selected(self, algorithm_panel):
        algorithm_panel.srtf_checkbox.setChecked(True)

        algorithms = algorithm_panel.get_algorithms()

        assert len(algorithms) == 1
        assert isinstance(algorithms[0], SRTF_Scheduler)

    def test_round_robin_selected(self, algorithm_panel):
        algorithm_panel.rr_checkbox.setChecked(True)
        algorithm_panel.quantum_input.setValue(5)

        algorithms = algorithm_panel.get_algorithms()

        assert len(algorithms) == 1
        assert isinstance(algorithms[0], RoundRobin_Scheduler)
        assert algorithms[0].quantum == 5

    def test_multiple_algorithms_selected(self, algorithm_panel):
        algorithm_panel.fcfs_checkbox.setChecked(True)
        algorithm_panel.sjf_checkbox.setChecked(True)
        algorithm_panel.srtf_checkbox.setChecked(True)
        algorithm_panel.rr_checkbox.setChecked(True)

        algorithm_panel.quantum_input.setValue(4)

        algorithms = algorithm_panel.get_algorithms()

        assert len(algorithms) == 4

        assert isinstance(algorithms[0], FCFS_Scheduler)
        assert isinstance(algorithms[1], SJF_Scheduler)
        assert isinstance(algorithms[2], SRTF_Scheduler)
        assert isinstance(algorithms[3], RoundRobin_Scheduler)

        assert algorithms[3].quantum == 4

    def test_quantum_minimum(self, algorithm_panel):
        algorithm_panel.rr_checkbox.setChecked(True)

        algorithm_panel.quantum_input.setValue(1)

        assert algorithm_panel.quantum_input.value() == 1

    def test_quantum_maximum(self, algorithm_panel):
        algorithm_panel.rr_checkbox.setChecked(True)

        algorithm_panel.quantum_input.setValue(100)

        assert algorithm_panel.quantum_input.value() == 100

    def test_reset(self, algorithm_panel):
        algorithm_panel.fcfs_checkbox.setChecked(True)
        algorithm_panel.sjf_checkbox.setChecked(True)
        algorithm_panel.srtf_checkbox.setChecked(True)
        algorithm_panel.rr_checkbox.setChecked(True)
        algorithm_panel.quantum_input.setValue(10)

        algorithm_panel.reset()

        assert not algorithm_panel.fcfs_checkbox.isChecked()
        assert not algorithm_panel.sjf_checkbox.isChecked()
        assert not algorithm_panel.srtf_checkbox.isChecked()
        assert not algorithm_panel.rr_checkbox.isChecked()

        assert algorithm_panel.quantum_input.value() == 2
        assert not algorithm_panel.quantum_input.isEnabled()
        assert not algorithm_panel.quantum_label.isEnabled()