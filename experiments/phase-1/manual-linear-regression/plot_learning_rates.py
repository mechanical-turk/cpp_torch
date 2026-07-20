import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot loss trajectories from the learning-rate experiment."
    )
    parser.add_argument("csv_path", type=Path, help="Experiment CSV to plot")
    return parser.parse_args()


@dataclass
class Trajectory:
    epochs: list[int] = field(default_factory=list)
    w_values: list[float] = field(default_factory=list)
    b_values: list[float] = field(default_factory=list)
    losses: list[float] = field(default_factory=list)


def load_trajectories(csv_path: Path) -> dict[float, Trajectory]:
    trajectories: dict[float, Trajectory] = defaultdict(Trajectory)

    with csv_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            learning_rate = float(row["learning_rate"])
            trajectory = trajectories[learning_rate]
            trajectory.epochs.append(int(row["epoch"]))
            trajectory.w_values.append(float(row["w"]))
            trajectory.b_values.append(float(row["b"]))
            trajectory.losses.append(float(row["loss"]))

    return dict(trajectories)


def plot_loss_trajectories(
    trajectories: dict[float, Trajectory],
    output_path: Path,
) -> None:
    figure, axes = plt.subplots(figsize=(9, 6))

    for learning_rate, trajectory in sorted(trajectories.items()):
        axes.plot(
            trajectory.epochs,
            trajectory.losses,
            label=f"a = {learning_rate:.6g}",
        )

    axes.set_yscale("log")
    axes.set_title("Gradient-descent stability around the learning-rate boundary")
    axes.set_xlabel("Epoch")
    axes.set_ylabel("Mean squared error (log scale)")
    axes.grid(True, which="both", alpha=0.3)
    axes.legend()

    figure.tight_layout()
    figure.savefig(output_path, dpi=160)
    plt.close(figure)


def plot_parameter_trajectories(
    trajectories: dict[float, Trajectory],
    output_path: Path,
) -> None:
    sorted_trajectories = sorted(trajectories.items())
    figure, axes = plt.subplots(
        nrows=len(sorted_trajectories),
        ncols=2,
        figsize=(12, 10),
        sharex=True,
        squeeze=False,
    )

    for row, (learning_rate, trajectory) in enumerate(sorted_trajectories):
        w_axes, b_axes = axes[row]
        w_axes.plot(trajectory.epochs, trajectory.w_values, color="tab:blue")
        b_axes.plot(trajectory.epochs, trajectory.b_values, color="tab:orange")
        w_axes.axhline(2.0, color="black", linestyle="--", alpha=0.6)
        b_axes.axhline(1.0, color="black", linestyle="--", alpha=0.6)
        w_axes.set_ylabel(f"a = {learning_rate:.6g}\nSlope w")
        b_axes.set_ylabel("Intercept b")

        for parameter_axes in (w_axes, b_axes):
            parameter_axes.grid(True, alpha=0.3)

    axes[0, 0].set_title("Slope w (optimum = 2)")
    axes[0, 1].set_title("Intercept b (optimum = 1)")
    axes[-1, 0].set_xlabel("Epoch")
    axes[-1, 1].set_xlabel("Epoch")
    figure.suptitle("Parameter trajectories around the learning-rate boundary")

    figure.tight_layout()
    figure.savefig(output_path, dpi=160)
    plt.close(figure)


def main() -> None:
    args = parse_args()
    loss_output_path = Path("learning_rate_loss.png")
    parameters_output_path = Path("learning_rate_parameters.png")
    trajectories = load_trajectories(args.csv_path)
    plot_loss_trajectories(trajectories, loss_output_path)
    plot_parameter_trajectories(trajectories, parameters_output_path)
    print(f"Saved {loss_output_path}")
    print(f"Saved {parameters_output_path}")


if __name__ == "__main__":
    main()
