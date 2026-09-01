import pytest
from PySide6.QtWidgets import QApplication


from src.gui.workload_panel import WorkloadPanel
from src.gui.algorithm_panel import Algorithm_Panel
from src.gui.simulation_control_panel import SimulationControlPanel

@pytest.fixture(scope="session")
def app():
    application = QApplication.instance()

    if application is None:
        application = QApplication([])

    return application


@pytest.fixture
def workload_panel(app):
    return WorkloadPanel()

@pytest.fixture
def algorithm_panel(app):
    return Algorithm_Panel()


@pytest.fixture
def simulation_control_panel(app):
    return SimulationControlPanel()
