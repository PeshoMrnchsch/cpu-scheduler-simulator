import matplotlib

matplotlib.use("Agg")

from src.metrics.result import SimulationResult
from src.visualization.comparison_visualiser import ComparisonVisualizer


def make_results(*entries):
    return {
        name: {
            "result": SimulationResult(
                processes_completed=[],
                simulation_start=start,
                simulation_end=end,
                cpu_timeline=timeline,
            ),
            "metrics": {},
        }
        for name, start, end, timeline in entries
    }


def test_empty_results_do_not_create_a_figure(capsys, monkeypatch):
    show_called = False

    def fail_if_called():
        nonlocal show_called
        show_called = True

    monkeypatch.setattr("matplotlib.pyplot.show", fail_if_called)

    ComparisonVisualizer({}).show()

    assert show_called is False
    assert "No processes were executed." in capsys.readouterr().out


def test_one_algorithm_creates_one_labeled_row(monkeypatch):
    shown_figures = []
    monkeypatch.setattr(
        "matplotlib.pyplot.show",
        lambda: shown_figures.append(matplotlib.pyplot.gcf()),
    )
    results = make_results(
        ("FCFS", 0, 5, [(0, 2, 1), (2, 5, 2)])
    )

    ComparisonVisualizer(results).show()

    assert len(shown_figures) == 1
    figure = shown_figures[0]
    assert len(figure.axes) == 1
    assert figure.axes[0].get_ylabel() == "FCFS"


def test_all_algorithm_rows_share_global_time_limits(monkeypatch):
    shown_figures = []
    monkeypatch.setattr(
        "matplotlib.pyplot.show",
        lambda: shown_figures.append(matplotlib.pyplot.gcf()),
    )
    results = make_results(
        ("FCFS", 0, 5, [(0, 5, 1)]),
        ("SJF", 2, 9, [(2, 9, 2)]),
        ("SRTF", 1, 7, [(1, 7, 3)]),
        ("Round Robin", 0, 8, [(0, 2, 1), (2, 8, 2)]),
    )

    ComparisonVisualizer(results).show()

    axes = shown_figures[0].axes
    assert len(axes) == 4
    assert all(axis.get_xlim() == (0.0, 9.0) for axis in axes)
    assert [axis.get_ylabel() for axis in axes] == [
        "FCFS",
        "SJF",
        "SRTF",
        "Round Robin",
    ]


def test_empty_cpu_timeline_is_labeled_without_a_rectangle(monkeypatch):
    shown_figures = []
    monkeypatch.setattr(
        "matplotlib.pyplot.show",
        lambda: shown_figures.append(matplotlib.pyplot.gcf()),
    )
    results = make_results(
        ("FCFS", 0, 5, []),
        ("SJF", 0, 5, [(0, 5, 1)]),
    )

    ComparisonVisualizer(results).show()

    empty_axis = shown_figures[0].axes[0]
    assert len(empty_axis.patches) == 0
    assert [text.get_text() for text in empty_axis.texts] == ["No CPU activity"]


def test_idle_interval_uses_idle_color(monkeypatch):
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)
    results = make_results(
        ("FCFS", 0, 5, [(0, 2, 1), (2, 5, None)])
    )

    ComparisonVisualizer(results).show()

    idle_patch = matplotlib.pyplot.gcf().axes[0].patches[1]
    assert idle_patch.get_facecolor()[:3] == matplotlib.colors.to_rgb("lightgray")


def test_process_ids_beyond_palette_cycle_safely(monkeypatch):
    monkeypatch.setattr("matplotlib.pyplot.show", lambda: None)
    results = make_results(
        ("FCFS", 0, 2, [(0, 1, 100), (1, 2, 101)])
    )

    ComparisonVisualizer(results).show()

    assert len(matplotlib.pyplot.gcf().axes[0].patches) == 2