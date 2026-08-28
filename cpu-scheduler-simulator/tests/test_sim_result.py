from src.model.process import Process
from src.metrics.result import SimulationResult


class TestSimulationResult:

    def test_stores_completed_processes(self):
        p1 = Process(1, 0, 5)
        p2 = Process(2, 1, 3)

        result = SimulationResult(
            [p1, p2],
            0,
            8,
            [(0, 5, 1), (5, 8, 2)]
        )

        assert result.processes_completed == [p1, p2]

    def test_stores_simulation_start(self):
        result = SimulationResult([], 0, 10, [])

        assert result.simulation_start == 0

    def test_stores_simulation_end(self):
        result = SimulationResult([], 0, 10, [])

        assert result.simulation_end == 10

    def test_stores_timeline(self):
        timeline = [
            (0, 3, 1),
            (3, 5, 2),
            (5, 7, 1)
        ]

        result = SimulationResult([], 0, 7, timeline)

        assert result.timeline == timeline

    def test_stores_cpu_and_io_timelines_independently(self):
        cpu_timeline = [(0, 3, 1)]
        io_timeline = [(1, 4, 1)]

        result = SimulationResult([], 0, 4, cpu_timeline, io_timeline)

        assert result.cpu_timeline == cpu_timeline
        assert result.io_timeline == io_timeline
        assert result.timeline is result.cpu_timeline

    def test_empty_process_list(self):
        result = SimulationResult([], 0, 0, [])

        assert result.processes_completed == []
        assert result.simulation_start == 0
        assert result.simulation_end == 0
        assert result.timeline == []

    def test_idle_timeline_is_preserved(self):
        timeline = [
            (0, 3, 1),
            (3, 6, None),
            (6, 8, 2)
        ]

        result = SimulationResult([], 0, 8, timeline)

        assert result.timeline == timeline

    def test_process_order_is_preserved(self):
        p1 = Process(1, 0, 2)
        p2 = Process(2, 0, 3)
        p3 = Process(3, 0, 1)

        processes = [p2, p1, p3]

        result = SimulationResult(processes, 0, 6, [])

        assert result.processes_completed == [p2, p1, p3]

    def test_timeline_order_is_preserved(self):
        timeline = [
            (0, 2, 2),
            (2, 4, 1),
            (4, 5, 3)
        ]

        result = SimulationResult([], 0, 5, timeline)

        assert result.timeline == [
            (0, 2, 2),
            (2, 4, 1),
            (4, 5, 3)
        ]

    def test_single_process_simulation(self):
        p1 = Process(1, 0, 5)

        result = SimulationResult(
            [p1],
            0,
            5,
            [(0, 5, 1)]
        )

        assert len(result.processes_completed) == 1
        assert result.simulation_end == 5
        assert result.timeline == [(0, 5, 1)]