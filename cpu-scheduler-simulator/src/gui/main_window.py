import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
)
from src.gui.workload_panel import WorkloadPanel
from src.gui.algorithm_panel import Algorithm_Panel
from src.gui.simulation_control_panel import SimulationControlPanel
from src.gui.results_panel import ResultsPanel
from src.gui.gantt_chart import GanttPanel
from src.metrics.comparison import Comparison


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CPU Scheduler Simulator")
        self.resize(1200, 800)
        
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        main_layout = QVBoxLayout(container)
        
        scroll_area.setWidget(container)

        self.setCentralWidget(scroll_area)     
        
        # Top layout
        top_layout = QHBoxLayout()

        self.workload_panel = WorkloadPanel()
        self.alg_panel = Algorithm_Panel()
        
        top_layout.addWidget(self.workload_panel)
        top_layout.addWidget(self.alg_panel)

        # Bottom Layout
        self.sim_control_panel = SimulationControlPanel()
        self.results_panel = ResultsPanel()
        self.gantt_panel  = GanttPanel() 
        
        main_layout.addLayout(top_layout, 0)
        main_layout.addWidget(self.sim_control_panel, 0)
        main_layout.addWidget(self.results_panel, 0)
        main_layout.addWidget(self.gantt_panel , 3)
        
        self.sim_control_panel.run_clicked.connect(
            self.run_simulation
        )
        
        self.sim_control_panel.reset_clicked.connect(
            self.reset
        )
    
    def run_simulation(self):
        self.sim_control_panel.set_status("Running")
        try:
            
            workload = self.workload_panel.convert_to_workload()
            
            algs = self.alg_panel.get_algorithms()
            comp = Comparison(workload, algs).compare()
               
            self.results_panel.display_results(comp)
            
            self.gantt_panel.display_results(comp, "cpu")
            self.sim_control_panel.set_status("Completed")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Simulation Error",
                f"An error happened:\n{e}",
                QMessageBox.StandardButton.Ok,
            )
            self.sim_control_panel.set_status("Error")

    def reset(self):
        self.workload_panel.clear()
        self.alg_panel.reset()
        self.results_panel.clear()
        self.gantt_panel.clear()

        self.sim_control_panel.set_status("Ready")
        
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())