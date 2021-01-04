import sys

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

import plot

import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureManager


def add_slider(name, slider):
    globals()[f'slider_{name}'] = slider


def get_val(name):
    return globals()[f'slider_{name}'].val


# BASIC SLIDERS
slider_initial_infected = None
slider_contacts_per_day = None
slider_prob_of_infection_for_contact = None
slider_recover_rate = None
slider_birth_death_rate = None
slider_t = None

# SEIRS SLIDERS
slider_disease_transmission_rate = None


def make_model(fig: Figure):
    args = sys.argv
    if len(args) != 2:
        return -1
    if args[1] == "sir-model":
        plot.sir_model(fig)
    elif args[1] == "sir-vital":
        plot.sir_vital(fig)
    elif args[1] == "seirs-model":
        plot.seiers_model(fig)
    else:
        return -1
    return 0


def main():
    fig: Figure = plt.figure()

    if make_model(fig) is None:
        print("Invalid model type\nCurrently supported types: sir-model, sir-vital")
        return

    manager: FigureManager = plt.get_current_fig_manager()
    manager.set_window_title("SIR Model")
    manager.full_screen_toggle()

    fig.canvas.draw_idle()
    plt.show()


if __name__ == '__main__':
    main()
