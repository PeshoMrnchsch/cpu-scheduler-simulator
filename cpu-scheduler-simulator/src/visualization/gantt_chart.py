class GanttChart:
    UNIT_WIDTH = 6

    def __init__(self, timeline, type_result="cpu"):
        self.timeline = timeline
        self.type_result = type_result

    def _timeline_with_gaps(self):
        intervals = []
        previous_end = None

        for interval in self.timeline:
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
        if not self.timeline:
            print("No processes were executed.")
            return
        
        print(self.build_blocks())
        print(self.build_time_labels())
        
