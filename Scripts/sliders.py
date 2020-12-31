from matplotlib.figure import Figure
from matplotlib.widgets import Slider

import main


def initial_infected_sld(fig: Figure, init_cond, update, bottom):
    main.slider_initial_infected = Slider(fig.add_axes(
        [0.21, bottom, 0.6, 0.03]
    ), "Initial Infected (%)", 0.0, 10.0,
        valinit=init_cond.initial_infected_people / init_cond.total_people * 100,
        valstep=0.01,
    )
    main.slider_initial_infected.on_changed(update)


def update_initial_infected(cond):
    infected_percent = main.slider_initial_infected.val
    new_i0 = cond.total_people * infected_percent / 100
    new_s0 = cond.total_people - new_i0
    cond.initial_infected_people = new_i0
    cond.initial_susceptible_people = new_s0


def contacts_sld(fig: Figure, init_cond, update, bottom):
    main.slider_contacts = Slider(fig.add_axes(
        [0.21, bottom, 0.6, 0.03]
    ), "Contacts", 1.0, 25.0, valinit=init_cond.contacts_per_day, valstep=1.0)
    main.slider_contacts.on_changed(update)


def update_contacts(cond):
    cond.contacts_per_day = main.slider_contacts.val


def prob_sld(fig: Figure, init_cond, update, bottom):
    main.slider_probability = Slider(fig.add_axes(
        [0.21, bottom, 0.6, 0.03]
    ), "Infection prob.", 0.0, 1.0, valinit=init_cond.prob_of_infection_for_contact, valstep=0.001)
    main.slider_probability.on_changed(update)


def update_prob(cond):
    cond.prob_of_infection_for_contact = main.slider_probability.val


def recover_sld(fig: Figure, init_cond, update, bottom):
    main.slider_recover = Slider(fig.add_axes(
        [0.21, bottom, 0.6, 0.03]
    ), "Recover rate", 0.0, 0.5, valinit=init_cond.recover_rate, valstep=0.001)
    main.slider_recover.on_changed(update)


def update_recover(cond):
    cond.recover_rate = main.slider_recover.val


def birth_death_sld(fig: Figure, init_cond, update, bottom):
    main.slider_birth_death = Slider(fig.add_axes(
        [0.21, bottom, 0.6, 0.03]
    ), "Birth/Death Rate", 0.0, 0.2, valinit=init_cond.birth_death_rate, valstep=0.001)
    main.slider_birth_death.on_changed(update)


def update_birth_death(cond):
    cond.birth_death_rate = main.slider_birth_death.val


def time_sld(fig: Figure, init_cond, update, bottom):
    main.slider_time = Slider(fig.add_axes(
        [0.21, bottom, 0.6, 0.03]
    ), "Time", 10.0, 500.0, valinit=init_cond.t, valstep=1.0)
    main.slider_time.on_changed(update)


def update_t(cond):
    cond.t = main.slider_time.val


def sir_sliders(fig: Figure, init_cond, update):
    set_sliders(fig, init_cond, update, [
        initial_infected_sld, contacts_sld, prob_sld, recover_sld, time_sld
    ])


def sir_sliders_vital(fig: Figure, init_cond, update):
    set_sliders(fig, init_cond, update, [
        initial_infected_sld, contacts_sld, prob_sld, recover_sld, birth_death_sld, time_sld
    ])


def set_sliders(fig: Figure, init_cond, update, sliders):
    line_width = 0.05
    offset = 0.05
    for sld, i in zip(sliders, range(len(sliders))):
        sld(fig, init_cond, update, offset + i * line_width)


def update_sir(init_cond):
    return get_updater(init_cond, [
        update_initial_infected, update_contacts, update_prob, update_recover, update_t
    ])


def update_sir_vital(init_cond):
    return get_updater(init_cond, [
        update_initial_infected, update_contacts, update_prob, update_recover, update_birth_death, update_t,
    ])


def get_updater(init_cond, updates):
    def inner(val):
        for upd in updates:
            upd(init_cond)
    return inner
