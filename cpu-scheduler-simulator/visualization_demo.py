"""Console examples for checking CPU and I/O Gantt chart edge cases."""

from src.visualization.gantt_chart import GanttChart


def show_case(name, cpu_timeline, io_timeline):
    print("\n" + "=" * 72)
    print(name)
    print("=" * 72)

    print("CPU timeline:")
    GanttChart(cpu_timeline, "cpu").render()

    print("I/O timeline:")
    GanttChart(io_timeline, "io").render()


def main():
    show_case(
        "1. Normal CPU and I/O activity",
        cpu_timeline=[
            (0, 3, 1),
            (3, 5, 2),
            (5, 8, 1),
        ],
        io_timeline=[
            (1, 3, 1, 0),
            (4, 6, 2, 1),
        ],
    )

    show_case(
        "2. CPU idle period between process arrivals",
        cpu_timeline=[
            (0, 2, 1),
            (2, 7, None),
            (7, 9, 2),
        ],
        io_timeline=[],
    )

    show_case(
        "3. Empty CPU and I/O timelines",
        cpu_timeline=[],
        io_timeline=[],
    )

    show_case(
        "4. Different durations and back-to-back intervals",
        cpu_timeline=[
            (0, 1, 1),
            (1, 10, 2),
            (10, 11, 3),
        ],
        io_timeline=[
            (0, 1, 1, 0),
            (1, 8, 1, 0),
            (8, 9, 2, 1),
        ],
    )

    show_case(
        "5. Multiple I/O devices",
        cpu_timeline=[
            (0, 4, 1),
            (4, 6, 2),
        ],
        io_timeline=[
            (0, 2, 1, 0),
            (0, 3, 2, 1),
            (3, 5, 2, 2),
        ],
    )


if __name__ == "__main__":
    main()
