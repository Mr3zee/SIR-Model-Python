from matplotlib.figure import Figure
from matplotlib.widgets import Slider

import main


def slider_fabric(name, label, lower, upper, step):
    def inner(fig: Figure, init_cond, update, left, bottom, width, height):
        slider = Slider(fig.add_axes(
            [left, bottom, width, height]
        ), label, lower, upper, valinit=init_cond.get(name), valstep=step)
        slider.on_changed(update)
        main.add_slider(name, slider)

    def inner_update(cond):
        cond.set(name, main.get_val(name))

    return inner, inner_update


def initial_infected_sld(fig: Figure, init_cond, update, left, bottom, width, height):
    main.slider_initial_infected = Slider(fig.add_axes(
        [left, bottom, width, height]
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


contacts_sld, update_contacts = slider_fabric('contacts_per_day', 'Contacts', 1.0, 25.0, 1.0)
prob_sld, update_prob = slider_fabric('prob_of_infection_for_contact', 'Infection prob.', 0.0, 1.0, 0.001)
recover_sld, update_recover = slider_fabric('recover_rate', 'Recover rate', 0.0, 0.5, 0.001)
birth_death_sld, update_birth_death = slider_fabric('birth_death_rate', 'Birth/Death Rate', 0.0, 0.2, 0.001)
time_sld, update_time = slider_fabric('t', 'Time', 10.0, 500.0, 1.0)


###############################################################################################
# SEIRS SLIDERS
###############################################################################################


init_infected_symp_sld, update_init_infected_symp = slider_fabric('initial_symptomatic_infected', 'Init. Infected', 0.0, 0.5, 0.001)
alpha_sld, update_alpha = slider_fabric('disease_transmission_rate', 'Dis. trans.', 0.1, 1.0, 0.001)
g_sld, update_g = slider_fabric('recovered_lose_immunity_rate', 'Lose Immunity', 0.0, 0.01, 0.0001)
mu_sld, update_mu = slider_fabric('average_incubation_period', 'Incub. Period', 0.0, 14.0, 0.1)
f_sld, update_f = slider_fabric('reinfected_carriers_rate', 'Reinf. Carriers', 0.0, 2.0, 0.001)
r_sld, update_r = slider_fabric('exposed_to_symptomatic_infected_rate', 'Exposed', 0.0, 2.0, 0.001)
epsilon_sld, update_epsilon = slider_fabric('infected_to_quarantined_rate', 'Inf. to Quar.', 0.0, 1.0, 0.001)
zetta1_sld, update_zetta1 = slider_fabric('infected_to_deceased_rate', 'Inf. to Dec.', 0.0, 1.0, 0.001)
eta1_sld, update_eta1 = slider_fabric('infected_to_disabled_rate', 'Inf. to Dis.', 0.0, 1.0, 0.001)
beta3_sld, update_beta3 = slider_fabric('asymptomatic_recovery_rate', 'Asymp. Recovery', 0.0, 1.0, 0.0001)
zetta3_sld, update_zetta3 = slider_fabric('asymptomatic_death_rate', 'Asymp. Death', 0.0, 1.0, 0.001)
eta3_sld, update_eta3 = slider_fabric('asymptomatic_disability_rate', 'Asymp. Disability', 0.0, 0.5, 0.001)
v_sld, update_v = slider_fabric('quarantined_to_carrier_rate', 'Quar. to Carrier', 0.0, 1.0, 0.001)
ro_sld, update_ro = slider_fabric('quarantined_to_icu_rate', 'Quar. to ICU', 0.0, 1.0, 0.001)
zetta2_sld, update_zetta2 = slider_fabric('quarantined_to_deceased_rate', 'Quar. to Dec.', 0.0, 1.0, 0.001)
eta2_sld, update_eta2 = slider_fabric('quarantined_to_disabled_rate', 'Quar. to Dis.', 0.0, 1.0, 0.001)
beta1_sld, update_beta1 = slider_fabric('quarantined_recovery_rate', 'Quar. Recovery', 0.0, 1.0, 0.001)
beta4_sld, update_beta4 = slider_fabric('icu_recover_rate', 'ICU Recovery', 0.0, 1.0, 0.001)
zetta5_sld, update_zetta5 = slider_fabric('icu_death_rate', 'ICU Death', 0.0, 1.0, 0.001)
eta5_sld, update_eta5 = slider_fabric('icu_disable_rate', 'ICU Dis.', 0.0, 1.0, 0.001)
beta2_sld, update_beta2 = slider_fabric('carrier_recover_rate', 'Car. Recover', 0.0, 1.0, 0.0001)
zetta4_sld, update_zetta4 = slider_fabric('carrier_death_rate', 'Car. Death', 0.0, 1.0, 0.001)
eta4_sld, update_eta4 = slider_fabric('carrier_disable_rate', 'Car. Dis.', 0.0, 1.0, 0.001)


###############################################################################################


def sir_sliders(fig: Figure, init_cond, update):
    set_sliders(fig, init_cond, update, [
        initial_infected_sld, contacts_sld, prob_sld, recover_sld, time_sld
    ], 0.21, 0.6, 0.03, 0.05)


def sir_vital_sliders(fig: Figure, init_cond, update):
    set_sliders(fig, init_cond, update, [
        initial_infected_sld, contacts_sld, prob_sld, recover_sld, birth_death_sld, time_sld
    ], 0.21, 0.6, 0.03, 0.05)


def seirs_sliders(fig: Figure, init_cond, update):
    set_sliders(fig, init_cond, update, [
        init_infected_symp_sld, time_sld,
        alpha_sld, g_sld, mu_sld, f_sld, r_sld, epsilon_sld, zetta1_sld, eta1_sld,
        beta3_sld, zetta3_sld, eta3_sld, v_sld, ro_sld, zetta2_sld, eta2_sld,
        beta1_sld, beta4_sld, zetta5_sld, eta5_sld, beta2_sld, zetta4_sld, eta4_sld,
    ], 0.705, 0.25, 0.02, 0.04)


def set_sliders(fig: Figure, init_cond, update, sliders, left, width, height, line_height):
    offset = 0.05
    for sld, i in zip(sliders, range(len(sliders))):
        sld(fig, init_cond, update, left, offset + i * line_height, width, height)


def update_sir(init_cond):
    return get_updater(init_cond, [
        update_initial_infected, update_contacts, update_prob, update_recover, update_time
    ])


def update_sir_vital(init_cond):
    return get_updater(init_cond, [
        update_initial_infected, update_contacts, update_prob, update_recover, update_birth_death, update_time,
    ])


def update_seirs(init_cond):
    return get_updater(init_cond, [
        update_init_infected_symp, update_time,
        update_alpha, update_g, update_mu, update_f, update_r, update_epsilon, update_zetta1, update_eta1,
        update_beta3, update_zetta3, update_eta3, update_v, update_ro, update_zetta2, update_eta2,
        update_beta1, update_beta4, update_zetta5, update_eta5, update_beta2, update_zetta4, update_eta4,
    ])


def get_updater(init_cond, updates):
    def inner(val):
        for upd in updates:
            upd(init_cond)
    return inner
