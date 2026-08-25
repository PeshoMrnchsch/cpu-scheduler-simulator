import pytest

from src.model.process import Process
from src.metrics.metrics import Metrics


class TestMetrics:

    def test_turnaround_time(self):
        p1 = Process(1, 0, 5)
        p1.completion_time = 5

        metrics = Metrics([p1], 0, 5)

        assert metrics.turnaround_time(p1) == 5

    def test_waiting_time(self):
        p1 = Process(1, 0, 5)
        p1.completion_time = 8

        metrics = Metrics([p1], 0, 8)

        assert metrics.waiting_time(p1) == 3

    def test_average_turnaround_time(self):
        p1 = Process(1, 0, 5)
        p2 = Process(2, 0, 3)

        p1.completion_time = 5
        p2.completion_time = 8

        metrics = Metrics([p1, p2], 0, 8)

        assert metrics.average_turnaround_time() == 6.5

    def test_average_waiting_time(self):
        p1 = Process(1, 0, 5)
        p2 = Process(2, 0, 3)

        p1.completion_time = 5
        p2.completion_time = 8

        metrics = Metrics([p1, p2], 0, 8)

        assert metrics.average_waiting_time() == 2.5

    def test_empty_processes(self):
        metrics = Metrics([], 0, 0)

        assert metrics.average_turnaround_time() == 0.0
        assert metrics.average_waiting_time() == 0.0

    def test_cpu_utilization(self):
        timeline = [
            (0, 3, 1),
            (3, 5, None),
            (5, 8, 2)
        ]

        metrics = Metrics([], 0, 8, timeline)

        assert metrics.cpu_utilization() == 75.0

    def test_cpu_utilization_no_time(self):
        metrics = Metrics([], 0, 0, [])

        assert metrics.cpu_utilization() == 0.0

    def test_calculate(self):
        p1 = Process(1, 0, 5)
        p1.completion_time = 5

        timeline = [
            (0, 5, 1)
        ]

        metrics = Metrics([p1], 0, 5, timeline)

        result = metrics.calculate()

        assert result == {
            "average_turnaround_time": 5.0,
            "average_waiting_time": 0.0,
            "cpu_utilization": 100.0
        }