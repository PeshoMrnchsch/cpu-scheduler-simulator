from src.gui.simulation_control_panel import SimulationControlPanel


class TestSimulationControlPanel:

    def test_initial_state(self, simulation_control_panel):
        assert simulation_control_panel.status_label.text() == "Ready"

    def test_run_button_emits_signal(self, simulation_control_panel, qtbot):
        with qtbot.waitSignal(
            simulation_control_panel.run_clicked,
            timeout=1000
        ):
            simulation_control_panel.run_button.click()

    def test_reset_button_emits_signal(self, simulation_control_panel, qtbot):
        with qtbot.waitSignal(
            simulation_control_panel.reset_clicked,
            timeout=1000
        ):
            simulation_control_panel.reset_button.click()


    def test_run_button_exists(self, simulation_control_panel):
        assert simulation_control_panel.run_button is not None

    def test_reset_button_exists(self, simulation_control_panel):
        assert simulation_control_panel.reset_button is not None

    def test_status_label_exists(self, simulation_control_panel):
        assert simulation_control_panel.status_label is not None