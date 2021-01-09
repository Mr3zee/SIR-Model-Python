import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from model import SirModel, SirInitConditions, Model, SirVital, SeirsInitConditions, SeirsModel
import sliders
import main


def sir_model(fig: Figure):
    init_cond = SirInitConditions(
        t=50,
        total_people=main.sir_total,
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
        total_people=main.sir_vital_total,
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


def seirs_model(fig: Figure):
    total = main.seirs_total
    recovered = 33000
    cases = 100123
    active = cases - recovered
    exposed = 45061
    icu = 2528
    deaths = 1584
    init_cond = SeirsInitConditions(
        t=50,
        total_people=total,
        initial_susceptible_people=total - cases + recovered * 0.17,
        initial_exposed=exposed,
        initial_symptomatic_infected=active,
        initial_asymptomatic_infected=active * 0.17,
        initial_quarantined=active * 0.19,
        initial_icu=icu,
        initial_carrier=recovered * 0.17,
        initial_recovered_without_disability=recovered * 0.6,
        initial_deceased=deaths,
        initial_recovered_with_disability=recovered * 0.4,
        disease_transmission_rate=0.8,  # alpha
        recovered_lose_immunity_rate=0.0001,  # g
        average_incubation_period=7,  # mu
        reinfected_carriers_rate=0.05,  # f
        exposed_to_symptomatic_infected_rate=0.14,  # r
        infected_to_quarantined_rate=0.2,  # epsilon
        infected_to_deceased_rate=0.021,  # zetta1
        infected_to_disabled_rate=(recovered * 0.6) / cases,  # eta1
        asymptomatic_recovery_rate=(1 / 7),  # beta3
        asymptomatic_death_rate=(1 / 7) * 0.021,  # zetta3
        asymptomatic_disability_rate=(1 / 7) * 0.4,  # eta3
        quarantined_to_carrier_rate=0.05,  # v
        quarantined_to_icu_rate=0.25,  # ro
        quarantined_to_deceased_rate=0.125,  # zetta2
        quarantined_to_disabled_rate=0.6,  # eta2
        quarantined_recovery_rate=(1 / 10),  # beta1
        icu_recover_rate=0.05,  # beta4
        icu_death_rate=0.5,  # zetta5
        icu_disable_rate=0.45,  # eta5
        carrier_recover_rate=(1 / 4),  # beta2
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

        ax.axis([0, init_cond.t, 0, init_cond.y])
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
