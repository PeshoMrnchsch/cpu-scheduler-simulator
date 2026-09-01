

fig, ax = plt.subplots()
ax.set_title("CPU Scheduling")
ax.set_xlabel("Time")
ax.set_ylabel("Resource")


for start, end, pid in result.cpu_timeline:
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


# plt.show()