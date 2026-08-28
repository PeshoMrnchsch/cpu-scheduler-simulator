import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class ComparisonVisualizer:
    IDLE_COLOR = "lightgray"
    
    def __init__(self, results:dict):
        self.results = results
            
    def show(self) -> None:
        if not self.results:
            print("No processes were executed.")
            return
        
        fig, axes = plt.subplots(
                    len(self.results),
                    1,
                    sharex=True,
                    squeeze=False
                )
        
        axes[-1, 0].set_xlabel("Simulation time")
        
        simulation_start = min(
            data["result"].simulation_start
            for data in self.results.values()
        )
        simulation_end = max(
            data["result"].simulation_end
            for data in self.results.values()
        )

        process_ids = sorted({
            pid
            for data in self.results.values()
            for _, _, pid in data["result"].cpu_timeline
            if pid is not None
        }, key=str)
        color_palette = plt.get_cmap("tab20").resampled(len(process_ids))
        color_map = {
            pid: color_palette(index)
            for index, pid in enumerate(process_ids)
        }

        
        for row, (alg_name, data) in enumerate(self.results.items()):
            
            result = data["result"]
            cpu_timeline = result.cpu_timeline
    
            current_axis = axes[row, 0]

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
        
        fig.suptitle("CPU Scheduling Comparison")
        fig.tight_layout()    
        plt.show()
        


            