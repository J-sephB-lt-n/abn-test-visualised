"""
Defines function 
simulate_cumulative_abn_test()
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
    ... group_names = ("treat", "control"),
    ... n_obs_per_period = (100, 30),
    ... true_success_rates = (0.05, 0.08),
    ... n_periods = 100,
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
    print(plot_colours)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
