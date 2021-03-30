import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureManager
from matplotlib.figure import Figure

import Scripts.plot as plot


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
slider_initial_symptomatic_infected = None


def make_model(fig: Figure):
    args = sys.argv
    if len(args) != 2:
        return -1
    if args[1] == "sir-model":
        plot.sir_model(fig)
    elif args[1] == "sir-vital":
        plot.sir_vital(fig)
    elif args[1] == "seirs-model":
        plot.seirs_model(fig)
    else:
        return -1
    return 0


def main():
    fig: Figure = plt.figure()

    if make_model(fig) == -1:
        print("Invalid model type\nCurrently supported types: sir-model, sir-vital, seirs-model")
        return

    manager: FigureManager = plt.get_current_fig_manager()
    manager.set_window_title("SIR Model")
    manager.full_screen_toggle()

    fig.canvas.draw_idle()
    plt.show()
