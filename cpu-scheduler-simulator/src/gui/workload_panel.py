from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem, 
    QHeaderView,
    QPushButton,
    QHBoxLayout
)
from PySide6.QtCore import Qt

from src.model.process import Process
from src.model.workload import Workload

class WorkloadPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        self.label = QLabel("Workload")

        self.add_button = QPushButton("Add Process")
        self.add_button.clicked.connect(
            self.add_empty_process
        )
        
        self.remove_button = QPushButton("Remove Process")
        self.remove_button.clicked.connect(
            self.remove_process
        )
        # self.button_layout()
        
        self.table = QTableWidget()
        
        self.table.setRowCount(0)
        
        self.table.setColumnCount(3)
        
        self.table.setHorizontalHeaderLabels([
            "PID",
            "Arrival",
            "Burst",
        ])
         
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        
        layout.addWidget(self.label)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

        self.setLayout(layout)
        
    
    def add_process(self, pid, arrival, burst):
        """Adds a process row"""
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)        
        self.table.setItem(
            row_count,
            0,
            QTableWidgetItem(str(pid))
        )

        self.table.setItem(
            row_count,
            1,
            QTableWidgetItem(str(arrival))
        )

        self.table.setItem(
            row_count,
            2,
            QTableWidgetItem(str(burst))
        )
        
           
    def remove_process(self):
        """Remove the currently selected process from the table."""

        current_row = self.table.currentRow()

        if current_row == -1:
            return

        self.table.removeRow(current_row)
        self.renumber_pids()
        
    def renumber_pids(self):
        
        for row in range(self.table.rowCount()):
            pid = f"P{row+1}"
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(pid))
            )
                        
    def convert_to_workload(self):
        """Converts table into Workload object"""

        if self.table.rowCount() == 0:
            raise ValueError("Workload cannot be empty.")

        processes = []
        used_pids = set()

        for row in range(self.table.rowCount()):
            row_number = row + 1

            pid_item = self.table.item(row, 0)

            if pid_item is None or not pid_item.text().strip():
                raise ValueError(
                    f"Row {row_number}: PID cannot be empty."
                )

            pid = pid_item.text().strip()

            if pid in used_pids:
                raise ValueError(
                    f"Row {row_number}: PID '{pid}' already exists."
                )

            used_pids.add(pid)

            arrival_item = self.table.item(row, 1)

            if arrival_item is None or not arrival_item.text().strip():
                raise ValueError(
                    f"Row {row_number}: Arrival time cannot be empty."
                )

            try:
                arrival = int(arrival_item.text().strip())
            except ValueError:
                raise ValueError(
                    f"Row {row_number}: Arrival time must be an integer."
                )

            if arrival < 0:
                raise ValueError(
                    f"Row {row_number}: Arrival time cannot be negative."
                )

            burst_item = self.table.item(row, 2)

            if burst_item is None or not burst_item.text().strip():
                raise ValueError(
                    f"Row {row_number}: Burst time cannot be empty."
                )

            try:
                burst = int(burst_item.text().strip())
            except ValueError:
                raise ValueError(
                    f"Row {row_number}: Burst time must be an integer."
                )

            if burst <= 0:
                raise ValueError(
                    f"Row {row_number}: Burst time must be greater than 0."
                )

            process = Process(pid, arrival, burst)
            processes.append(process)

        return Workload(processes)

    def add_empty_process(self):
        """Adds an empty process row to the table."""

        row = self.table.rowCount()
        
        self.table.insertRow(row)

        pid_item = QTableWidgetItem(f"P{row + 1}")
        pid_item.setFlags(pid_item.flags() & ~Qt.ItemIsEditable)

        self.table.setItem(row, 0, pid_item)
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setItem(row, 2, QTableWidgetItem(""))

        self.table.setCurrentCell(row, 1)
            
        
    def clear(self):
        """Remove all processes from the workload table."""
        self.table.setRowCount(0)