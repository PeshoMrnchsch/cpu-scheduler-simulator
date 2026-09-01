from PySide6.QtWidgets import (
QLabel,
QWidget,
QTableWidget,
QTableWidgetItem,
QHeaderView,
QVBoxLayout,
QSizePolicy,
)

class ResultsPanel(QWidget):
    MAX_RESULT_ROWS = 4

    def __init__(self):
        super().__init__()
        

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Results"))

        self.table = QTableWidget()
        
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        
        self.table.setHorizontalHeaderLabels([
            "Algorithm",
            "Avg Waiting Time",
            "Avg Turnaround Time",
            "CPU Utilization"
        ])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        vertical_header = self.table.verticalHeader()
        vertical_header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
            
        layout.addWidget(self.table)
        self.setLayout(layout)
        
    def display_results(self, comparisons: dict):
        self.table.setRowCount(0)
        
        for row, (alg, data) in enumerate(
            list(comparisons.items())[:self.MAX_RESULT_ROWS]
        ):
            avg_wait = data["metrics"]["average_waiting_time"]
            avg_turnaround = data["metrics"]["average_turnaround_time"]
            cpu_utilization = data["metrics"]["cpu_utilization"]
                        
            self.table.insertRow(row)    
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(alg)
            )    
            self.table.setItem(
                row,
                1,
                QTableWidgetItem(f"{avg_wait:.2f}")
            )
    
            self.table.setItem(
                row,
                2,
                QTableWidgetItem(f"{avg_turnaround:.2f}")
            )
    
            self.table.setItem(
                row,
                3,
                QTableWidgetItem(f"{cpu_utilization:.2f}%")
            )
    
    def clear(self):
        self.table.setRowCount(0)
