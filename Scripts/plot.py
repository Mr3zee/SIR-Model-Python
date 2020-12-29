import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from model import SirModel, SirInitConditions, Model, SirVital
import sliders


def sir_model(fig: Figure, ax: Axes):

    init_cond = SirInitConditions(
        total_people=10000,
        initial_infected_people=10,
        contacts_per_day=3,
        prob_of_infection_for_contact=0.5,
        recover_rate=.3,
        birth_death_rate=0,
    )

    build_model(
        fig=fig, ax=ax,
        init_cond=init_cond,
        update_init_cond=sliders.update_sir(init_cond),
        model=SirModel(init_cond),
        outlines=["g-", "y--", "r-"],
        labels=["S", "I", "R"],
        sliders_setter=sliders.sir_sliders,
        xlabel="Time, days", ylabel="s(t), i(t), r(t)", title="SIR Model"
    )


def sir_vital(fig: Figure, ax: Axes):

    init_cond = SirInitConditions(
        total_people=10000,
        initial_infected_people=10,
        contacts_per_day=3,
        prob_of_infection_for_contact=0.5,
        recover_rate=.3,
        birth_death_rate=0.2,
    )

    build_model(
        fig=fig, ax=ax,
        init_cond=init_cond,
        update_init_cond=sliders.update_sir_vital(init_cond),
        model=SirVital(init_cond),
        outlines=["g-", "y--", "r-"],
        labels=["S", "I", "R"],
        sliders_setter=sliders.sir_sliders_vital,
        xlabel="Time, days", ylabel="s(t), i(t), r(t)", title="SIR Model With Vital Dynamics"
    )


def build_model(
        fig: Figure,
        ax: Axes,
        init_cond,
        update_init_cond,
        model: Model,
        outlines: list,
        labels: list,
        sliders_setter,
        xlabel, ylabel, title,
):
    def update(val):
        update_init_cond(init_cond)

        model.ic = init_cond
        for plot, data in zip(plots, list(model.solve(time_axis).T)):
            plot.set_ydata(data)

        fig.canvas.draw_idle()

    time_axis = np.arange(0, 50)
    plots = [ax.plot(time_axis, fun, outline, label=label)[0]
             for fun, outline, label in zip(model.solve(time_axis).T, outlines, labels)]

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper right")
    ax.set_title(title)

    sliders_setter(fig, init_cond, update)
