from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)


class IOPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.devices = []

        layout = QVBoxLayout()

        layout.addWidget(QLabel("I/O Configuration"))

        # Selected process
        self.process_label = QLabel("Process: None")
        layout.addWidget(self.process_label)

        # I/O mode
        io_mode_layout = QHBoxLayout()

        io_mode_layout.addWidget(QLabel("I/O:"))

        self.io_mode = QComboBox()
        self.io_mode.addItems([
            "No I/O",
            "I/O",
        ])

        self.io_mode.currentTextChanged.connect(
            self.update_io_mode
        )

        io_mode_layout.addWidget(self.io_mode)

        layout.addLayout(io_mode_layout)

        # Device selection
        device_layout = QHBoxLayout()

        device_layout.addWidget(QLabel("Device:"))

        self.device_combo = QComboBox()
        self.device_combo.addItem("D0")
        self.devices.append("D0")

        device_layout.addWidget(self.device_combo)

        self.add_device_button = QPushButton("Add Device")
        self.add_device_button.clicked.connect(
            self.add_device
        )

        device_layout.addWidget(self.add_device_button)

        layout.addLayout(device_layout)

        # Add I/O button
        self.add_io_button = QPushButton("Add I/O")
        self.add_io_button.clicked.connect(
            self.add_io
        )

        layout.addWidget(self.add_io_button)

        # I/O table
        self.table = QTableWidget()

        self.table.setRowCount(0)
        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels([
            "Execution Point",
            "Duration",
            "Device",
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Remove I/O button
        self.remove_io_button = QPushButton("Remove I/O")
        self.remove_io_button.clicked.connect(
            self.remove_io
        )

        layout.addWidget(self.remove_io_button)

        self.setLayout(layout)

        self.update_io_mode("No I/O")

    def set_process(self, process):
        """Display the I/O configuration for the selected process."""

        self.process = process

        self.process_label.setText(
            f"Process: {process.pid}"
        )

        self.load_process_io()

    def load_process_io(self):
        """Load the selected process's I/O requests into the table."""

        self.table.setRowCount(0)

        if not hasattr(self, "process"):
            return

        if not self.process.io_requests:
            self.io_mode.setCurrentText("No I/O")
            return

        self.io_mode.setCurrentText("I/O")

        for request in self.process.io_requests:

            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(request.execution_point)
                )
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(request.duration)
                )
            )

            device_id = getattr(
                request.device,
                "device_id",
                str(request.device)
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(device_id)
                )
            )

    def update_io_mode(self, mode):
        """Enable or disable I/O controls."""

        has_io = mode == "I/O"

        self.device_combo.setEnabled(has_io)
        self.add_device_button.setEnabled(has_io)
        self.add_io_button.setEnabled(has_io)
        self.table.setEnabled(has_io)
        self.remove_io_button.setEnabled(has_io)

        if not has_io:
            self.table.setRowCount(0)

    def add_device(self):
        """Add a new I/O device."""

        device_number = len(self.devices)

        device_id = f"D{device_number}"

        self.devices.append(device_id)

        self.device_combo.addItem(device_id)
        self.device_combo.setCurrentText(device_id)

    def add_io(self):
        """Add an empty I/O request row."""

        if not hasattr(self, "process"):
            QMessageBox.warning(
                self,
                "No Process Selected",
                "Select a process before adding I/O."
            )
            return

        self.io_mode.setCurrentText("I/O")

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row,
            0,
            QTableWidgetItem("")
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem("")
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(
                self.device_combo.currentText()
            )
        )

        self.table.setCurrentCell(row, 0)

    def remove_io(self):
        """Remove the selected I/O request."""

        row = self.table.currentRow()

        if row == -1:
            return

        self.table.removeRow(row)

    def clear(self):
        """Clear the I/O panel."""

        self.process = None

        self.process_label.setText(
            "Process: None"
        )

        self.io_mode.setCurrentText("No I/O")

        self.table.setRowCount(0)

        self.devices = ["D0"]

        self.device_combo.clear()
        self.device_combo.addItem("D0")