"""
Shows animated result of simulated A/B/N test

Example usage:
    $ python main.py \
            --group_names treatment1,treatment2,control \
            --n_obs_per_day 50,50,50 \
            --true_rates 0.1,0.08,0.09 \
            --n_sim_days 20
"""

import argparse
import random

import matplotlib
import matplotlib.cm
import matplotlib.animation
import matplotlib.pyplot as plt

# python my_script_name.py abc def --debug --filename temp.html -n 69
parser = argparse.ArgumentParser()
parser.add_argument(
    "-g",
    "--group_names",
    help="Names of the experimental groups (used in the plot legend)",
    type=lambda input_string: input_string.split(","),
    required=True,
)
parser.add_argument(
    "-n",
    "--n_obs_per_day",
    help="Number of data points observed per day (per group)",
    type=lambda input_string: [int(x) for x in input_string.split(",")],
    required=True,
)
parser.add_argument(
    "-r",
    "--true_rates",
    help="True rate per group (per group)",
    type=lambda input_string: [float(x) for x in input_string.split(",")],
    required=True,
)
parser.add_argument("-d", "--n_sim_days", help="Number of days to simulate", type=int)
args = parser.parse_args()

matplotlib.use("Agg")

N_GROUPS = len(args.group_names)

plot_cmap = matplotlib.cm.get_cmap("viridis", N_GROUPS)

group_history = dict()
for grp_idx, grp_name in enumerate(args.group_names):
    group_history[grp_name] = {
        "n_obs_per_day": args.n_obs_per_day[grp_idx],
        "true_rate": args.true_rates[grp_idx],
        "successes_per_day": [
            sum(
                random.choices(
                    [0, 1],
                    weights=[1 - args.true_rates[grp_idx], args.true_rates[grp_idx]],
                    k=args.n_obs_per_day[grp_idx],
                )
            )
            for _ in range(args.n_sim_days)
        ],
        "cumulative_n_obs": [
            (day_count * args.n_obs_per_day[grp_idx])
            for day_count in range(1, args.n_sim_days + 1)
        ],
        "cumulative_n_successes": None,
        "cumulative_success_rate": None,
        "plot_colour": plot_cmap(grp_idx),
    }
    group_history[grp_name]["cumulative_n_successes"] = [
        sum(group_history[grp_name]["successes_per_day"][:day_idx])
        for day_idx in range(1, args.n_sim_days + 1)
    ]
    group_history[grp_name]["cumulative_success_rate"] = [
        n_success / n_obs
        for n_success, n_obs in zip(
            group_history[grp_name]["cumulative_n_successes"],
            group_history[grp_name]["cumulative_n_obs"],
        )
    ]

fig, ax = plt.subplots()

x = range(args.n_sim_days)
ax.set(
    xlim=(0, args.n_sim_days),
    # ylim=(0, 0.1),
    xlabel="Day",
    ylabel="Cumulative Open Rate",
)
grp_iter = iter(group_history.items())
grp_name, grp_info = next(grp_iter)
lineplot = ax.plot(
    x[0],
    grp_info["cumulative_success_rate"][0],
    label=grp_name,
    color=grp_info["plot_colour"],
)
ax.axhline(y=grp_info["true_rate"], color=grp_info["plot_colour"], alpha=0.5)
for grp_name, grp_info in grp_iter:
    ax.plot(
        x[0],
        grp_info["cumulative_success_rate"][0],
        label=grp_name,
        color=grp_info["plot_colour"],
    )
    ax.axhline(y=grp_info["true_rate"], color=grp_info["plot_colour"], alpha=0.5)

ax.legend()


def update_plot(frame_idx):
    grp_iter = iter(group_history.items())
    grp_name, grp_info = next(grp_iter)
    new_plot = ax.plot(
        x[:frame_idx],
        grp_info["cumulative_success_rate"][:frame_idx],
        label=grp_name,
        color=grp_info["plot_colour"],
    )
    for grp_name, grp_info in grp_iter:
        ax.plot(
            x[:frame_idx],
            grp_info["cumulative_success_rate"][:frame_idx],
            label=grp_name,
            color=grp_info["plot_colour"],
        )

    return new_plot


plt_anim = matplotlib.animation.FuncAnimation(
    fig=fig,
    func=update_plot,
    frames=range(args.n_sim_days),
    interval=100,  # delay between frames (milliseconds)
    repeat=True,
)

print("exporting gif to ./output.gif")
#plt_anim.save("./output.gif", writer="imagemagick", fps=5)
plt.show()
