import sys

from matplotlib.axes import Axes
from matplotlib.figure import Figure

import plot

import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureManager

slider_initial_infected = None
slider_contacts = None
slider_probability = None
slider_recover = None
slider_birth_death = None


def make_model(fig: Figure, ax: Axes):
    args = sys.argv
    if len(args) != 2:
        return -1
    if args[1] == "sir-model":
        plot.sir_model(fig, ax)
    elif args[1] == "sir-vital":
        plot.sir_vital(fig, ax)
    else:
        return -1
    return 0


def main():
    fig: Figure = plt.figure()
    ax: Axes = fig.add_axes([0.10, 0.35, 0.8, 0.6])

    if make_model(fig, ax) is None:
        print("Invalid model type\nCurrently supported types: sir-model, sir-vital")
        return

    manager: FigureManager = plt.get_current_fig_manager()
    manager.set_window_title("SIR Model")
    manager.resize(1440, 810)

    fig.canvas.draw_idle()
    plt.show()


if __name__ == '__main__':
    main()
