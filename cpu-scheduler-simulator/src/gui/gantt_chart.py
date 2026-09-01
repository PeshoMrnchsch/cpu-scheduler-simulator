from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg 
from matplotlib.figure import Figure

from src.visualization.gantt_chart import GanttChart

class GanttPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Gantt Chart"))

        self.figure = Figure(facecolor="none")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setStyleSheet("background: transparent;")

        layout.addWidget(self.canvas)

        self.setLayout(layout)
    
    def display_results(self, comparisons: dict, type_result: str = "cpu"):
        self.figure.clear()

        if not comparisons:
            self.canvas.draw()
            return

        num_algorithms = len(comparisons)

        dynamic_height = max(3, num_algorithms * 1.5)

        self.figure.set_size_inches(
            10,
            dynamic_height
        )

        axes = self.figure.subplots(
            num_algorithms,
            1,
            sharex=False
        )

        if num_algorithms == 1:
            axes = [axes]

        for ax, (alg, data) in zip(
            axes,
            comparisons.items()
        ):
            simulation_result = data["result"]
            timeline = simulation_result.timeline

            chart = GanttChart(
                timeline,
                type_result
            )

            chart.draw(ax)

            ax.set_title(
                alg,
                pad=6,
                fontsize=10,
                fontweight="bold"
            )

            ax.set_ylabel("CPU")
            ax.tick_params(axis="x", labelsize=8, pad=2)

            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            for tick in ax.get_xticklabels() + ax.get_yticklabels():
                tick.set_color("white")

            for text in ax.texts:
                text.set_color("white")

            for spine in ax.spines.values():
                spine.set_color("white")

        self.figure.tight_layout(
            pad=1.0,
            h_pad=0.8,
            rect=(0, 0.04, 1, 1)
        )

        self.canvas.setMinimumHeight(
            int(dynamic_height * 80)
        )

        self.canvas.draw()
    
    def clear(self):
        self.figure.clear()
        self.figure.patch.set_alpha(0)
        self.canvas.draw()