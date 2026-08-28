import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class GanttChart:
    UNIT_WIDTH = 6

    def __init__(self, result, type_result:str):
        self.results = result
        self.type_result = type_result

    def _timeline_with_gaps(self):
        intervals = []
        previous_end = None

        for interval in self.results:
            start, end = interval[:2]
            if previous_end is not None and start > previous_end:
                if self.type_result == "io":
                    intervals.append((previous_end, start, None, None))
                else:
                    intervals.append((previous_end, start, None))

            intervals.append(interval)
            previous_end = max(previous_end or end, end)

        return intervals

    def _label_and_width(self, interval):
        start, end, pid = interval[:3]
        duration = end - start

        if self.type_result == "io":
            device_id = interval[3]
            label = "IDLE" if device_id is None else f"P{pid} / D{device_id}"
        else:
            label = "IDLE" if pid is None else f"P{pid}"

        width = max(duration * self.UNIT_WIDTH, len(label) + 2)
        return label, width

    def build_blocks(self):
        chart = ""
        for interval in self._timeline_with_gaps():
            label, width = self._label_and_width(interval)
            chart += f"| {label:^{width}} "

        return chart + "|"

    def build_time_labels(self):
        labels = ""

        intervals = self._timeline_with_gaps()
        for interval in intervals:
            start = interval[0]
            _, width = self._label_and_width(interval)
            labels += f"{start:<{width + 3}}"

        final_end = intervals[-1][1]
        labels += str(final_end)

        return labels

    def render(self):
        if not self.results:
            print("No processes were executed.")
            return
        
        print(self.build_blocks())
        print(self.build_time_labels())
        
    def render_matplot(self):
        if not self.results:
            print("No processes were executed.")
            return

        fig, ax = plt.subplots()

        simulation_start = min(interval[0] for interval in self.results)
        simulation_end = max(interval[1] for interval in self.results)

        ax.set_xlim(simulation_start, simulation_end)
        ax.set_ylim(-0.2, 1)
        ax.set_yticks([0.4])
        ax.set_yticklabels(["CPU"])
        ax.set_xlabel("Simulation time")
        ax.grid(axis="x", linestyle="--", alpha=0.4)
        
        if self.type_result == "cpu":
            for start, end, pid in self.results:
                label = "IDLE" if pid is None else f"P{pid}"
                color = "lightgray" if pid is None else "cornflowerblue"

                ax.add_patch(
                    Rectangle(
                        (start, 0),
                        end - start,
                        0.8,
                        facecolor=color,
                        edgecolor="black"
                    )
                )

                ax.text(
                    (start + end) / 2,
                    0.4,
                    label,
                    ha="center",
                    va="center"
                )

        plt.show()
        # elif self.type_result == "io":
        #     for start, end, pid, device_id in result.io_timeline:
        #         row = device_id + 1

        #         ax.add_patch(
        #             Rectangle(
        #                 (start, row),
        #                 end - start,
        #                 0.8,
        #                 facecolor="seagreen",
        #                 edgecolor="black"
        #             )
        #         )

        #         ax.text(
        #             (start + end) / 2,
        #             row + 0.4,
        #             f"P{pid}",
        #             ha="center",
        #             va="center"
        #         )
            
timeline = [
    (0, 3, 1),
    (3, 5, 2),
    (5, 7, 1)
]
chart = GanttChart(timeline, type_result="cpu")
# chart.render_matplot()