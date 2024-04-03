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

import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

print(args.group_names)
print(args.n_obs_per_day)
print(args.true_rates)
print(args.n_sim_days)

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

from pprint import pprint

pprint(group_history)
"""
fig, ax = plt.subplots()

x = range(N_PERIODS)
y = [random.uniform(0.0, 0.1) for _ in range(N_PERIODS)]

lineplot = ax.plot(x[0], y[0], label="y", color="red")
ax.set(xlim=(0, N_PERIODS), ylim=(0, 0.1), xlabel="Period", ylabel="y")
ax.legend()


def update_plot(frame_idx):
    new_plot = ax.plot(x[:frame_idx], y[:frame_idx], color="red")
    return new_plot


plt_anim = animation.FuncAnimation(
    fig=fig,
    func=update_plot,
    frames=range(N_PERIODS),
    interval=500,  # delay between frames (milliseconds)
)
plt.show()
"""
