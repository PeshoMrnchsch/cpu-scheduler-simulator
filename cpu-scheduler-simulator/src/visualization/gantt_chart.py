class GanttChart:

    def __init__(self, timeline):
        self.timeline = timeline

    def build_blocks(self):
        chart = ""

        for start, end, pid in self.timeline:

            if pid is None:
                label = "IDLE"
            else:
                label = f"P{pid}"

            chart += f"| {label:^5} "

        return chart + "|"

    def build_time_labels(self):
        labels = ""

        for start, end, pid in self.timeline:
            labels += f"{start:<8}"

        labels += str(self.timeline[-1][1])

        return labels

    def render(self):
        if not self.timeline:
            print("No processes were executed.")
            return
        
        print(self.build_blocks())
        print(self.build_time_labels())
        
