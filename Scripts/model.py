from abc import ABC, abstractmethod

from scipy.integrate import odeint


class InitCond:
    def get(self, item):
        return getattr(self, item)

    def set(self, item, value):
        setattr(self, item, value)


class SirInitConditions(InitCond):
    def __init__(
            self,
            t,
            total_people,
            initial_infected_people,
            contacts_per_day,
            prob_of_infection_for_contact,
            recover_rate,
            birth_death_rate
    ):
        # validate it
        self.t = t
        self.y = total_people
        self.total_people = total_people
        self.initial_susceptible_people = total_people - initial_infected_people
        self.initial_infected_people = initial_infected_people
        self.initial_recovered_people = 0
        self.contacts_per_day = contacts_per_day
        self.prob_of_infection_for_contact = prob_of_infection_for_contact
        self.recover_rate = recover_rate
        self.birth_death_rate = birth_death_rate

    def n(self):
        return self.total_people

    def n1(self):
        return self.initial_susceptible_people

    def n2(self):
        return self.initial_infected_people

    def n3(self):
        return self.initial_recovered_people

    def m(self):
        return self.contacts_per_day

    def p(self):
        return self.prob_of_infection_for_contact

    def gamma(self):
        return self.recover_rate

    def d(self):
        return self.birth_death_rate

    def beta(self):
        return self.m() * self.p()

    def r0(self):
        return self.beta() / self.gamma()

    def beta_tilde(self):
        return self.beta() / self.n()


class Model(ABC):
    ic = None

    def __init__(self, init_cond):
        self.ic = init_cond

    @abstractmethod
    def _get_start_conditions(self):
        pass

    @abstractmethod
    def _model(self, sir0, t):
        pass

    def solve(self, time_linspace):
        return odeint(self._model, self._get_start_conditions(), time_linspace)


class SirModel(Model, ABC):
    def _get_start_conditions(self):
        return [self.ic.n1(), self.ic.n2(), self.ic.n3()]

    def _model(self, sir0, t):
        s = sir0[0]
        i = sir0[1]
        r = sir0[2]
        dsdt = -self.ic.beta_tilde() * s * i
        didt = (self.ic.beta_tilde() * s - self.ic.gamma()) * i
        drdt = self.ic.gamma() * i
        return [dsdt, didt, drdt]


class SirVital(Model, ABC):
    def _get_start_conditions(self):
        return [self.ic.n1(), self.ic.n2(), self.ic.n3()]

    def _model(self, sir0, t):
        s = sir0[0]
        i = sir0[1]
        r = sir0[2]
        dsdt = -self.ic.beta_tilde() * s * i + self.ic.d() * (self.ic.n() - s)
        didt = (self.ic.beta_tilde() * s - self.ic.gamma() - self.ic.d()) * i
        drdt = self.ic.gamma() * i - self.ic.d() * r
        return [dsdt, didt, drdt]


class SeirsInitConditions(InitCond):
    def __init__(
            self,
            t,
            total_people,
            initial_susceptible_people,
            initial_exposed,
            initial_symptomatic_infected,
            initial_asymptomatic_infected,
            initial_quarantined,
            initial_icu,
            initial_carrier,
            initial_recovered_without_disability,
            initial_deceased,
            initial_recovered_with_disability,
            disease_transmission_rate,
            recovered_lose_immunity_rate,
            average_incubation_period,
            reinfected_carriers_rate,
            exposed_to_symptomatic_infected_rate,
            infected_to_quarantined_rate,
            infected_to_deceased_rate,
            infected_to_disabled_rate,
            asymptomatic_recovery_rate,
            asymptomatic_death_rate,
            asymptomatic_disability_rate,
            quarantined_to_carrier_rate,
            quarantined_to_icu_rate,
            quarantined_to_deceased_rate,
            quarantined_to_disabled_rate,
            quarantined_recovery_rate,
            icu_recover_rate,
            icu_death_rate,
            icu_disable_rate,
            carrier_recover_rate,
            carrier_death_rate,
            carrier_disable_rate
    ):
        self.t = t
        self.y = total_people
        self.initial_susceptible_people = initial_susceptible_people
        self.total_people = total_people
        self.disease_transmission_rate = disease_transmission_rate
        self.initial_recovered_with_disability = initial_recovered_with_disability
        self.initial_deceased = initial_deceased
        self.initial_recovered_without_disability = initial_recovered_without_disability
        self.initial_carrier = initial_carrier
        self.initial_icu = initial_icu
        self.initial_quarantined = initial_quarantined
        self.initial_asymptomatic_infected = initial_asymptomatic_infected
        self.initial_symptomatic_infected = initial_symptomatic_infected
        self.initial_exposed = initial_exposed
        self.carrier_disable_rate = carrier_disable_rate
        self.carrier_death_rate = carrier_death_rate
        self.carrier_recover_rate = carrier_recover_rate
        self.icu_disable_rate = icu_disable_rate
        self.icu_death_rate = icu_death_rate
        self.icu_recover_rate = icu_recover_rate
        self.quarantined_recovery_rate = quarantined_recovery_rate
        self.quarantined_to_disabled_rate = quarantined_to_disabled_rate
        self.quarantined_to_deceased_rate = quarantined_to_deceased_rate
        self.quarantined_to_icu_rate = quarantined_to_icu_rate
        self.quarantined_to_carrier_rate = quarantined_to_carrier_rate
        self.asymptomatic_disability_rate = asymptomatic_disability_rate
        self.asymptomatic_death_rate = asymptomatic_death_rate
        self.asymptomatic_recovery_rate = asymptomatic_recovery_rate
        self.infected_to_disabled_rate = infected_to_disabled_rate
        self.infected_to_deceased_rate = infected_to_deceased_rate
        self.infected_to_quarantined_rate = infected_to_quarantined_rate
        self.exposed_to_symptomatic_infected_rate = exposed_to_symptomatic_infected_rate
        self.reinfected_carriers_rate = reinfected_carriers_rate
        self.average_incubation_period = average_incubation_period
        self.recovered_lose_immunity_rate = recovered_lose_immunity_rate

    def n(self):
        return self.total_people

    def n1(self):
        return self.initial_susceptible_people

    def n2(self):
        return self.initial_exposed

    def n3(self):
        return self.initial_symptomatic_infected

    def n4(self):
        return self.initial_asymptomatic_infected

    def n5(self):
        return self.initial_quarantined

    def n6(self):
        return self.initial_icu

    def n7(self):
        return self.initial_carrier

    def n8(self):
        return self.initial_recovered_without_disability

    def n9(self):
        return self.initial_deceased

    def n10(self):
        return self.initial_recovered_with_disability

    def alpha(self):
        return self.disease_transmission_rate

    def g(self):
        return self.recovered_lose_immunity_rate

    def mu(self):
        return self.average_incubation_period

    def f(self):
        return self.reinfected_carriers_rate

    def r(self):
        return self.exposed_to_symptomatic_infected_rate

    def eps(self):
        return self.infected_to_quarantined_rate

    def xi_1(self):
        return self.infected_to_deceased_rate

    def eta_1(self):
        return self.infected_to_disabled_rate

    def beta_3(self):
        return self.asymptomatic_recovery_rate

    def xi_3(self):
        return self.asymptomatic_death_rate

    def eta_3(self):
        return self.asymptomatic_disability_rate

    def v(self):
        return self.quarantined_to_carrier_rate

    def ro(self):
        return self.quarantined_to_icu_rate

    def xi_2(self):
        return self.quarantined_to_deceased_rate

    def eta_2(self):
        return self.quarantined_to_disabled_rate

    def beta_1(self):
        return self.quarantined_recovery_rate

    def beta_4(self):
        return self.icu_recover_rate

    def xi_5(self):
        return self.icu_death_rate

    def eta_5(self):
        return self.icu_disable_rate

    def beta_2(self):
        return self.carrier_recover_rate

    def xi_4(self):
        return self.carrier_death_rate

    def eta_4(self):
        return self.carrier_disable_rate


class SeirsModel(Model, ABC):

    def _get_start_conditions(self):
        return [self.ic.n1(), self.ic.n2(), self.ic.n3(), self.ic.n4(), self.ic.n5(), self.ic.n6(),
                self.ic.n7(), self.ic.n8(), self.ic.n9(), self.ic.n10()]

    def _model(self, seirs, t):
        s = seirs[0]
        e = seirs[1]
        i_s = seirs[2]
        i_as = seirs[3]
        q = seirs[4]
        q_ap = seirs[5]
        c = seirs[6]
        r_wd = seirs[7]
        d = seirs[8]
        r_d = seirs[9]

        dsdt = -self.ic.alpha() / self.ic.n() * s * (i_s + i_as + c) + self.ic.g() * r_wd
        dedt = self.ic.alpha() / self.ic.n() * s * (i_s + i_as + c) - self.ic.mu() * e
        di_sdt = self.ic.r() * self.ic.mu() * e - self.ic.eps() * i_s + self.ic.f() * c - self.ic.xi_1() * i_s - self.ic.eta_1() * i_s
        di_asdt = (1 - self.ic.r()) * self.ic.mu() * e - self.ic.beta_3() * i_as - self.ic.xi_3() * i_as - self.ic.eta_3() * i_as
        dqdt = self.ic.eps() * i_s - self.ic.beta_1() * q - self.ic.v() * q - self.ic.ro() * q - self.ic.xi_2() * q - self.ic.eta_2() * q
        dq_apdt = self.ic.ro() * q - self.ic.beta_4() * q_ap - self.ic.xi_5() * q_ap - self.ic.eta_5() * q_ap
        dcdt = self.ic.v() * q - self.ic.f() * c - self.ic.beta_2() * c - self.ic.xi_4() * c - self.ic.eta_4() * c
        dr_wddt = self.ic.beta_1() * q + self.ic.beta_3() * i_as + self.ic.beta_2() * c - self.ic.g() * r_wd
        dddt = self.ic.xi_1() * i_s + self.ic.xi_2() * q + self.ic.xi_3() * i_as + self.ic.xi_4() * c + self.ic.xi_5() * q_ap
        drddt = self.ic.eta_1() * i_s + self.ic.eta_2() * q + self.ic.eta_3() * i_as + self.ic.eta_4() * c + self.ic.eta_5() * q_ap

        return [dsdt, dedt, di_sdt, di_asdt, dqdt, dq_apdt, dcdt, dr_wddt, dddt, drddt]
