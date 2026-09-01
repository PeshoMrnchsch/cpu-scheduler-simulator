from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QSpinBox,
)

from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.scheduler_algorithms.SJF import SJF_Scheduler
from src.scheduler_algorithms.SRTF import SRTF_Scheduler
from src.scheduler_algorithms.RoundRobin import RoundRobin_Scheduler


class Algorithm_Panel(QWidget):  # EDITED: inherit from QWidget

    def __init__(self):
        super().__init__()

        self.fcfs_checkbox = QCheckBox("FCFS")
        self.sjf_checkbox = QCheckBox("SJF")
        self.srtf_checkbox = QCheckBox("SRTF")
        self.rr_checkbox = QCheckBox("Round Robin")

        self.quantum_label = QLabel("Quantum:")

        self.quantum_input = QSpinBox()
        self.quantum_input.setMinimum(1)
        self.quantum_input.setMaximum(100)
        self.quantum_input.setValue(2)

        # Round Robin is initially disabled
        self.quantum_label.setEnabled(False)
        self.quantum_input.setEnabled(False)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Algorithms"))

        layout.addWidget(self.fcfs_checkbox)
        layout.addWidget(self.sjf_checkbox)
        layout.addWidget(self.srtf_checkbox)
        layout.addWidget(self.rr_checkbox)

        quantum_layout = QHBoxLayout()
        quantum_layout.addWidget(self.quantum_label)
        quantum_layout.addWidget(self.quantum_input)

        layout.addLayout(quantum_layout)

        self.setLayout(layout)

        self.rr_checkbox.stateChanged.connect(
            self.update_algorithm_options
        )

    def update_algorithm_options(self):
        """Enable Round Robin options when Round Robin is selected."""

        enabled = self.rr_checkbox.isChecked()

        self.quantum_label.setEnabled(enabled)
        self.quantum_input.setEnabled(enabled)

    def get_algorithms(self):
        """Return the algorithms selected by the user."""

        algorithms = []

        if self.fcfs_checkbox.isChecked():
            algorithms.append(FCFS_Scheduler())

        if self.sjf_checkbox.isChecked():
            algorithms.append(SJF_Scheduler())

        if self.srtf_checkbox.isChecked():
            algorithms.append(SRTF_Scheduler())

        if self.rr_checkbox.isChecked():
            quantum = self.quantum_input.value()
            algorithms.append(RoundRobin_Scheduler(quantum))

        if not algorithms:
            raise ValueError("At least one algorithm must be selected.")

        return algorithms
    
    def reset(self):
        """Reset all algorithm selections and Round Robin options."""

        # Uncheck all algorithms
        self.fcfs_checkbox.setChecked(False)
        self.sjf_checkbox.setChecked(False)
        self.srtf_checkbox.setChecked(False)
        self.rr_checkbox.setChecked(False)

        # Restore default Round Robin quantum
        self.quantum_input.setValue(2)

        # Disable Round Robin options
        self.quantum_label.setEnabled(False)
        self.quantum_input.setEnabled(False)