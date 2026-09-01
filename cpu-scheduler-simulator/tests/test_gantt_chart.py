from src.visualization.gantt_chart import GanttChart
from src.model.process import Process
from src.model.workload import Workload
from src.scheduler_algorithms.RoundRobin import RoundRobin_Scheduler
from src.scheduler_algorithms.FCFS import FCFS_Scheduler
from src.scheduler_algorithms.SJF import SJF_Scheduler
from src.scheduler_algorithms.SRTF import SRTF_Scheduler
from src.simulator import Simulator


def test_cpu_entries_render_correctly():
    chart = GanttChart([(0, 2, 1), (2, 3, 2)], "cpu")

    blocks = chart.build_blocks()

    assert "P1" in blocks
    assert "P2" in blocks


def test_io_entries_with_device_render_correctly():
    chart = GanttChart([(0, 2, 1, 0)], "io")

    assert "P1 / D0" in chart.build_blocks()


def test_idle_cpu_entries_display_idle():
    chart = GanttChart([(0, 2, None)], "cpu")

    assert "IDLE" in chart.build_blocks()


def test_empty_timeline_does_not_crash(capsys):
    GanttChart([], "cpu").render()

    assert "No processes were executed." in capsys.readouterr().out


def test_time_labels_include_final_end_time():
    chart = GanttChart([(0, 2, 1), (2, 5, 2)], "cpu")

    assert chart.build_time_labels().endswith("5")


def test_different_durations_produce_different_block_widths():
    short_block = GanttChart([(0, 1, 1)], "cpu").build_blocks()
    long_block = GanttChart([(0, 3, 1)], "cpu").build_blocks()

    assert len(long_block) > len(short_block)


def test_missing_cpu_time_is_rendered_as_an_idle_gap():
    chart = GanttChart([(0, 1, 1), (3, 4, 2)], "cpu")

    blocks = chart.build_blocks()

    assert "IDLE" in blocks
    assert chart.build_time_labels().endswith("4")


def test_missing_io_time_is_rendered_as_an_idle_gap():
    chart = GanttChart([(0, 1, 1, 0), (3, 4, 2, 1)], "io")

    assert "IDLE" in chart.build_blocks()


def test_round_robin_cpu_timeline_renders_time_slices():
    workload = Workload([
        Process(process_id=1, arrival_time=0, burst_time=5),
        Process(process_id=2, arrival_time=0, burst_time=3),
    ])
    simulatorRR = Simulator(workload, FCFS_Scheduler())
    simulatorFcfs = Simulator(workload, RoundRobin_Scheduler(quantum=2))
    simulatorRR = Simulator(workload, RoundRobin_Scheduler(quantum=2))
    simulatorRR = Simulator(workload, RoundRobin_Scheduler(quantum=2))

    result = simulatorRR.run()
    chart = GanttChart(result.cpu_timeline, "cpu")

    assert result.cpu_timeline == [
        (0, 2, 1),
        (2, 4, 2),
        (4, 6, 1),
        (6, 7, 2),
        (7, 8, 1),
    ]
    assert "P1" in chart.build_blocks()
    assert "P2" in chart.build_blocks()
    assert chart.build_time_labels().endswith("8")