import matplotlib.pyplot as plt
import numpy as np
from matplotlib import interactive
from matplotlib.axes import Axes
from matplotlib.backends.backend_template import FigureManager
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

from model import SirModel, SirInitConditions

init_cond = SirInitConditions(
    total_people=10000,
    initial_susceptible_people=9990,
    initial_infected_people=10,
    initial_recovered_people=0,
    contacts_per_day=3,
    prob_of_infection_for_contact=0.5,
    recover_rate=.3,
    birth_death_rate=0,
)


def main():
    def update(val):

        infected_percent = slider_initial_infected.val
        new_i0 = init_cond.total_people * infected_percent / 100
        new_s0 = init_cond.total_people - new_i0
        init_cond.initial_infected_people = new_i0
        init_cond.initial_susceptible_people = new_s0

        init_cond.contacts_per_day = slider_contacts.val
        init_cond.prob_of_infection_for_contact = slider_probability.val
        init_cond.recover_rate = slider_recover.val

        model.ic = init_cond
        s_new, i_new, r_new = model.solve_sir(t).T

        s_plot.set_ydata(s_new)
        i_plot.set_ydata(i_new)
        r_plot.set_ydata(r_new)

        fig.canvas.draw_idle()

    fig: Figure = plt.figure()
    ax: Axes = fig.add_axes([0.10, 0.35, 0.8, 0.6])

    model = SirModel(init_cond)
    t = np.arange(0, 50)
    s, i, r = model.solve_sir(t).T

    s_plot = plt.plot(t, s, "g-", label="S")[0]
    i_plot = plt.plot(t, i, "y--", label="I")[0]
    r_plot = plt.plot(t, r, "r-", label="R")[0]

    ax.margins(x=0)
    ax.set_xlabel("Time, days")
    ax.set_ylabel("s(t), i(t), r(t)")
    ax.legend(loc="upper right")
    ax.set_title("SIR Model")

    slider_initial_infected = Slider(fig.add_axes(
        [0.21, 0.25, 0.6, 0.03]
    ), "Initial Infected (%)", 0.0, 50.0,
        valinit=init_cond.initial_infected_people / init_cond.total_people * 100,
        valstep=0.1,
    )

    slider_contacts = Slider(fig.add_axes(
        [0.21, 0.2, 0.6, 0.03]
    ), "Contacts", 1.0, 25.0, valinit=init_cond.contacts_per_day, valstep=1.0)

    slider_probability = Slider(fig.add_axes(
        [0.21, 0.15, 0.6, 0.03]
    ), "Infection prob.", 0.0, 1.0, valinit=init_cond.prob_of_infection_for_contact, valstep=0.01)

    slider_recover = Slider(fig.add_axes(
        [0.21, 0.1, 0.6, 0.03]
    ), "Recover rate", 0.0, 5.0, valinit=init_cond.recover_rate, valstep=0.1)

    slider_initial_infected.on_changed(update)
    slider_contacts.on_changed(update)
    slider_probability.on_changed(update)
    slider_recover.on_changed(update)

    manager: FigureManager = plt.get_current_fig_manager()
    manager.set_window_title("SIR Model")
    manager.resize(1440, 810)

    plt.show()


if __name__ == '__main__':
    main()
