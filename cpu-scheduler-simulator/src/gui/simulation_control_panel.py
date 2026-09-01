from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)

from PySide6.QtCore import Signal

class SimulationControlPanel(QWidget):
    run_clicked = Signal()
    reset_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.run_button = QPushButton("Run")
        
        self.reset_button = QPushButton("Reset")
        
        self.status_label = QLabel("Ready")
        
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Simulation"))

        layout.addWidget(self.run_button)
        layout.addWidget(self.reset_button)

        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Signals
        # Button click => emit custom signal
        self.run_button.clicked.connect(
            self.run_clicked.emit
        )

        self.reset_button.clicked.connect(
            self.reset_clicked.emit
        )

    def set_status(self, message:str):
        """Update the status displayed to the user."""

        self.status_label.setText(
            f"Status: {message}"
        )
