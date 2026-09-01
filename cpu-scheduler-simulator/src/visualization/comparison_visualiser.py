import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
 

def _simulation_limits(results):
    return (
        min(data["result"].simulation_start for data in results.values()),
        max(data["result"].simulation_end for data in results.values()),
    )

def _process_colors(results):
    process_ids = sorted({
        pid
        for data in results.values()
        for timeline in (
            data["result"].cpu_timeline,
            data["result"].io_timeline,
        )
        for interval in timeline
        for pid in [interval[2]]
        if pid is not None
    }, key=str)
    palette = plt.get_cmap("tab20").resampled(max(1, len(process_ids)))
    return {
        pid: palette(index)
        for index, pid in enumerate(process_ids)
    }
class ComparisonVisualizer:
    IDLE_COLOR = "lightgray"
    
    def __init__(self, results:dict):
        self.results = results
            
    def draw_on(self, fig, axes) -> None: 
        
        if not self.results:
            return
        
        simulation_start, simulation_end = _simulation_limits(self.results)
        color_map = _process_colors(self.results)
        for row, (alg_name, data) in enumerate(self.results.items()):
            
            result = data["result"]
            cpu_timeline = result.cpu_timeline

            current_axis = axes[row]
            if not cpu_timeline:
                current_axis.text(
                    (simulation_start + simulation_end) / 2,
                    0.4,
                    "No CPU activity",
                    ha="center",
                    va="center",
                    color="dimgray"
                )
            else:
                for start, end, pid in cpu_timeline:
                    if pid is None:
                        label = "IDLE"
                        color = self.IDLE_COLOR
                    else:
                        label = f"P{pid}"
                        color = color_map[pid]

                    width = end - start
                    current_axis.add_patch(
                        Rectangle(
                            (start, 0),
                            width,
                            0.8,
                            facecolor=color,
                            edgecolor="black"
                        )
                    )
                    current_axis.text(
                        start + width / 2,
                        0.4,
                        label,
                        ha="center",
                        va="center"
                    )
            current_axis.set_ylim(0, 1)
            current_axis.set_xlim(simulation_start, simulation_end)
            current_axis.grid(axis="x", linestyle="--", alpha=0.4)
            current_axis.set_ylabel(alg_name)
                    
        axes[-1].set_xlabel("Simulation time")
        
class IOComparisonVisualizer:
    IDLE_COLOR = "lightgray"

    def __init__(self, results: dict):
        self.results = results

    def rows(self):
        return [
            (alg_name, device_id)
            for alg_name, data in self.results.items()
            for device_id in sorted({
                interval[3]
                for interval in data["result"].io_timeline
            }, key=str)
        ]

    def draw_on(self, fig, axes) -> None:
        if not self.results:
            return

        simulation_start, simulation_end = _simulation_limits(self.results)
        color_map = _process_colors(self.results)
        io_rows = self.rows()

        if not io_rows:
            axes[0].text(
                (simulation_start + simulation_end) / 2,
                0.4,
                "No I/O activity",
                ha="center",
                va="center",
                color="dimgray",
            )
            axes[0].set_ylabel("I/O")
            axes[0].set_ylim(0, 1)
        else:
            for row, (alg_name, device_id) in enumerate(io_rows):
                current_axis = axes[row]
                timeline = self.results[alg_name]["result"].io_timeline
                device_timeline = [
                    interval
                    for interval in timeline
                    if interval[3] == device_id
                ]

                for start, end, pid, _ in device_timeline:
                    label = f"P{pid}"
                    current_axis.add_patch(
                        Rectangle(
                            (start, 0),
                            end - start,
                            0.8,
                            facecolor=color_map[pid],
                            edgecolor="black",
                        )
                    )
                    current_axis.text(
                        (start + end) / 2,
                        0.4,
                        label,
                        ha="center",
                        va="center",
                    )

                current_axis.set_ylabel(f"{alg_name} / D{device_id}")
                current_axis.set_ylim(0, 1)

        for axis in axes:
            axis.set_xlim(simulation_start, simulation_end)
            axis.grid(axis="x", linestyle="--", alpha=0.4)

        axes[-1].set_xlabel("Simulation time")
class MetricsTableVisualiser():
    def __init__(self, results:dict):
        self.results = results  
            
    def draw_on(self, axis) -> None: 
        if not self.results:
            return
        
        columns = [
                "Algorithm",
                "Avg. Turnaround",
                "Avg. Waiting",
                "CPU Utilization"
        ]
        
        
        final_data = []
        for alg_name, data in self.results.items():
            metrics = data["metrics"]
            
            row = [
                alg_name,
                f"{metrics['average_turnaround_time']:.2f}",
                f"{metrics['average_waiting_time']:.2f}",
                f"{metrics['cpu_utilization']:.2f}%"
            ]
            final_data.append(row)
        
        axis.axis("off")
        
        table = axis.table(
            cellText=final_data,
            colLabels=columns,
            loc="center"
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.8)     
       
class SimulationReportVisualizer:

    def __init__(self, results: dict):
        self.results = results

    def show(self) -> None:
        if not self.results:
            print("No processes were executed.")
            return

        # Create ONE shared figure
        fig = plt.figure(figsize=(12, 8))

        io_visualizer = IOComparisonVisualizer(self.results)
        io_rows = io_visualizer.rows()

        gs = fig.add_gridspec(
            3,
            1,
            height_ratios=[3, max(1, len(io_rows)), 1]
        )

        # Create comparison axes
        comparison_gs = gs[0].subgridspec(
            len(self.results),
            1
        )

        comparison_axes = [
            fig.add_subplot(comparison_gs[row, 0])
            for row in range(len(self.results))
        ]
        for axis in comparison_axes[1:]:
            axis.sharex(comparison_axes[0])

        io_gs = gs[1].subgridspec(max(1, len(io_rows)), 1)
        io_axes = [
            fig.add_subplot(io_gs[row, 0])
            for row in range(max(1, len(io_rows)))
        ]
        for axis in io_axes[1:]:
            axis.sharex(io_axes[0])

        table_axis = fig.add_subplot(gs[2])

        # Let visualizers draw onto existing axes
        comparison_visualizer = ComparisonVisualizer(
            self.results
        )

        metrics_visualizer = MetricsTableVisualiser(
            self.results
        )

        comparison_visualizer.draw_on(
            fig,
            comparison_axes
        )

        io_visualizer.draw_on(
            fig,
            io_axes
        )

        metrics_visualizer.draw_on(
            table_axis
        )

        # Figure title and spacing
        fig.suptitle("CPU Scheduling Comparison")

        fig.tight_layout(
            rect=[0, 0, 1, 0.95]
        )

        # Display ONE figure
        plt.show()
