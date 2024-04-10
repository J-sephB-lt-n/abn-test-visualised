"""
Defines function 
simulate_cumulative_abn_test()

local test:
    $ python understanding/experiment_design/simulate_cumulative_abn_test.py
"""

import random
from typing import Final

import matplotlib.cm
import matplotlib.animation
import matplotlib.pyplot as plt


def simulate_cumulative_abn_test(
    group_names: tuple[str, ...],
    n_obs_per_period: tuple[int, ...],
    true_success_rates: tuple[float, ...],
    n_periods: int,
    gif_export_path: str | None = None,
):
    """
    Simulates an a/b/n test and visualises it with an animation
    (where data is collected cumulatively over multiple periods)

    Args:
        group_names (tuple): The names of the experimental groups
        n_obs_per_period (tuple): Number of observations per period (for each group)
        true_success_rates (tuple): The true success rate in each group
                                    This is (obviously) unknown to the experimenter
        n_periods (int): Number of periods to simulate
        gif_export_path (:obj:`str`, optional): If included, exports the animation as a
                                                GIF to this path

    Example:
    >>> simulate_cumulative_abn_test(
    ... group_names = ("Treatment Group", "Control Group"),
    ... n_obs_per_period = (100, 20),
    ... true_success_rates = (0.05, 0.06),
    ... n_periods = 200,
    ... )
    """
    N_GROUPS: Final[int] = len(group_names)
    for var in (group_names, n_obs_per_period, true_success_rates):
        if len(var) != N_GROUPS:
            raise ValueError(
                "Arguments {group_names, "
                "n_obs_period_period, "
                "true_success_rates} must all "
                "have the same length"
            )
    plot_cmap = matplotlib.colormaps["viridis"]
    plot_colours = [plot_cmap(x / (N_GROUPS - 1)) for x in range(N_GROUPS)]

    sim_data = dict()
    for grp_idx, grp_name in enumerate(group_names):
        sim_data[grp_name] = {
            "n_obs_per_period": n_obs_per_period[grp_idx],
            "true_success_rate": true_success_rates[grp_idx],
            "n_success_in_period": [
                sum(
                    random.choices(
                        [0, 1],
                        weights=[
                            1 - true_success_rates[grp_idx],
                            true_success_rates[grp_idx],
                        ],
                        k=n_obs_per_period[grp_idx],
                    )
                )
                for period_num in range(1, n_periods + 1)
            ],
            "cumulative_n_obs": [
                (period_num * n_obs_per_period[grp_idx])
                for period_num in range(1, n_periods + 1)
            ],
            "cumulative_n_success": None,
            "cumulative_success_rate": None,
            "plot_colour": plot_colours[grp_idx],
        }
        sim_data[grp_name]["cumulative_n_success"] = [
            sum(sim_data[grp_name]["n_success_in_period"][:period_idx])
            for period_idx in range(1, n_periods + 1)
        ]
        sim_data[grp_name]["cumulative_success_rate"] = [
            n_success / n_obs
            for n_success, n_obs in zip(
                sim_data[grp_name]["cumulative_n_success"],
                sim_data[grp_name]["cumulative_n_obs"],
            )
        ]

    fig, axs = plt.subplots(2, 1, figsize=(10, 5))
    if len(sim_data) == 2:
        plt.suptitle("Simulated A/B Test")
    else:
        plt.suptitle("Simulated A/B/n Test")
    x = range(n_periods)
    axs[0].set(ylabel="Sample Size\n(cumulative)")
    axs[1].set(xlabel="Period", ylabel="Observed Success Rate\n(cumulative)")
    grp_iter = iter(sim_data.items())
    for grp_name, grp_info in grp_iter:
        axs[0].plot(
            x[0],
            grp_info["cumulative_n_obs"][0],
            label=grp_name,
            color=grp_info["plot_colour"],
        )
        axs[1].plot(
            x[0],
            grp_info["cumulative_success_rate"][0],
            label=f"Observed Success Rate: {grp_name}",
            color=grp_info["plot_colour"],
        )
        axs[1].axhline(
            y=grp_info["true_success_rate"],
            linestyle="dotted",
            color=grp_info["plot_colour"],
            label=f"True success rate: {grp_name}",
        )
    axs[0].legend(loc="upper left")

    def update_plot(frame_idx):
        grp_iter = iter(sim_data.items())
        for grp_name, grp_info in grp_iter:
            axs[0].plot(
                x[:frame_idx],
                grp_info["cumulative_n_obs"][:frame_idx],
                label=grp_name,
                color=grp_info["plot_colour"],
            )
            axs[1].plot(
                x[:frame_idx],
                grp_info["cumulative_success_rate"][:frame_idx],
                label=f"Observed Success Rate: {grp_name}",
                color=grp_info["plot_colour"],
            )
        return axs

    plt_anim = matplotlib.animation.FuncAnimation(
        fig=fig,
        func=update_plot,
        frames=range(n_periods),
        interval=200,  # delay between frames (milliseconds)
        repeat=True,
    )

    plt.show()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
