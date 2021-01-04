import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from model import SirModel, SirInitConditions, Model, SirVital, SeirsInitConditions, SeirsModel
import sliders


def sir_model(fig: Figure):

    init_cond = SirInitConditions(
        t=50,
        total_people=10000,
        initial_infected_people=10,
        contacts_per_day=3,
        prob_of_infection_for_contact=0.5,
        recover_rate=.3,
        birth_death_rate=0,
    )

    build_model(
        fig=fig, plot_position=[0.10, 0.35, 0.8, 0.6],
        init_cond=init_cond,
        update_init_cond=sliders.update_sir(init_cond),
        model=SirModel(init_cond),
        outlines=["g-", "y--", "r-"],
        labels=["S", "I", "R"],
        sliders_setter=sliders.sir_sliders,
        xlabel="Time, days", ylabel="Population", title="SIR Model"
    )


def sir_vital(fig: Figure):

    init_cond = SirInitConditions(
        t=70,
        total_people=10000,
        initial_infected_people=10,
        contacts_per_day=5,
        prob_of_infection_for_contact=0.1,
        recover_rate=.2,
        birth_death_rate=0.02,
    )

    build_model(
        fig=fig, plot_position=[0.10, 0.4, 0.8, 0.55],
        init_cond=init_cond,
        update_init_cond=sliders.update_sir_vital(init_cond),
        model=SirVital(init_cond),
        outlines=["g-", "y--", "r-"],
        labels=["S", "I", "R"],
        sliders_setter=sliders.sir_vital_sliders,
        xlabel="Time, days", ylabel="Population", title="SIR Model With Vital Dynamics"
    )


def seiers_model(fig: Figure):
    init_cond = SeirsInitConditions(
        t=50,
        total_people=1,
        initial_susceptible=0.9,
        initial_exposed=0,
        initial_symptomatic_infected=0.1,
        initial_asymptomatic_infected=0,
        initial_quarantined=0,
        initial_icu=0,
        initial_carrier=0,
        initial_recovered_without_disability=0,
        initial_deceased=0,
        initial_recovered_with_disability=0,
        disease_transmission_rate=0.42,  # alpha
        recovered_lose_immunity_rate=0.0001,  # g
        average_incubation_period=0.5,  # mu
        reinfected_carriers_rate=0.2,  # f
        exposed_to_symptomatic_infected_rate=0.3,  # r
        infected_to_quarantined_rate=0.5,  # epsilon
        infected_to_deceased_rate=0.25,  # zetta1
        infected_to_disabled_rate=0.1,  # eta1
        asymptomatic_recovery_rate=0.1458,  # beta3
        asymptomatic_death_rate=0.1,  # zetta3
        asymptomatic_disability_rate=0.05,  # eta3
        quarantined_to_carrier_rate=0.05,  # v
        quarantined_to_icu_rate=0.01,  # ro
        quarantined_to_deceased_rate=0.2,  # zetta2
        quarantined_to_disabled_rate=0.1,  # eta2
        quarantined_recovery_rate=0.5,  # beta1
        icu_recover_rate=0.05,  # beta4
        icu_death_rate=0.2,  # zetta5
        icu_disable_rate=0.1,  # eta5
        carrier_recover_rate=0.1458,  # beta2
        carrier_death_rate=0.05,  # zetta4
        carrier_disable_rate=0.01,  # eta4
    )

    build_model(
        fig=fig, plot_position=[0.05, 0.08, 0.55, 0.85],
        init_cond=init_cond,
        update_init_cond=sliders.update_seirs(init_cond),
        model=SeirsModel(init_cond),
        outlines=["g-", "b-", "y-", "y--", "r--", "r-", "c-", "k:", "k-", "k--"],
        labels=["S", "E", "I_s", "I_as", "Q", "Q'", "C", "R_wd", "D", "R_d"],
        sliders_setter=sliders.seirs_sliders,
        xlabel="Time, days", ylabel="Population", title="SEIRS Model"
    )


def build_model(
        fig: Figure,
        plot_position: list,
        init_cond,
        update_init_cond,
        model: Model,
        outlines: list,
        labels: list,
        sliders_setter,
        xlabel, ylabel, title,
):
    def update(val):
        if update_init_cond is not None:
            update_init_cond(init_cond)

        model.ic = init_cond
        new_time_axis = np.arange(0, int(init_cond.t))
        for plot, data in zip(plots, list(model.solve(new_time_axis).T)):
            plot.set_ydata(data)
            plot.set_xdata(new_time_axis)

        ax.axis([0, init_cond.t, 0, init_cond.total_people])
        fig.canvas.draw_idle()

    ax: Axes = fig.add_axes(plot_position)

    time_axis = np.arange(0, init_cond.t)
    plots = [ax.plot(time_axis, fun, outline, label=label)[0]
             for fun, outline, label in zip(model.solve(time_axis).T, outlines, labels)]

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper right")
    ax.set_title(title)
    ax.axis([0, init_cond.t, 0, init_cond.total_people])

    if sliders_setter is not None:
        sliders_setter(fig, init_cond, update)
