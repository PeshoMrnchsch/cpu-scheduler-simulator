class MetricsTable:

    def __init__(self, comparison_results):
        self.comparison_results = comparison_results

    def render(self):
        if not self.comparison_results:
            print("No comparison results available.")
            return

        print("\nAlgorithm Comparison")
        print("-" * 70)

        print(
            f"{'Algorithm':<15}"
            f"{'Avg. Turnaround':<20}"
            f"{'Avg. Waiting':<17}"
            f"{'CPU Utilization':<17}"
        )

        print("-" * 70)

        for algorithm, result in self.comparison_results.items():
            metrics = result["metrics"]

            turnaround = metrics["average_turnaround_time"]
            waiting = metrics["average_waiting_time"]
            cpu = metrics["cpu_utilization"]

            # FIX: Moved the '%' symbol outside the formatting expression
            print(
                f"{algorithm:<15}"
                f"{turnaround:<20.2f}"
                f"{waiting:<17.2f}"
                f"{cpu:<16.2f}%"
            )

comparison_results_1 = {
    "FCFS": {
        "metrics": {
            "average_turnaround_time": 6.33,
            "average_waiting_time": 3.00,
            "cpu_utilization": 100.0
        }
    },
    "SJF": {
        "metrics": {
            "average_turnaround_time": 5.67,
            "average_waiting_time": 2.33,
            "cpu_utilization": 100.0
        }
    },
    "SRTF": {
        "metrics": {
            "average_turnaround_time": 5.00,
            "average_waiting_time": 1.67,
            "cpu_utilization": 100.0
        }
    },
    "Round Robin": {
        "metrics": {
            "average_turnaround_time": 6.00,
            "average_waiting_time": 2.67,
            "cpu_utilization": 100.0
        }
    }
}
