import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class InitialConditions:
    def __init__(self,
                 total_people,
                 initial_susceptible_people,
                 initial_infected_people,
                 initial_recovered_people,
                 contacts_per_day,
                 prob_of_infection_for_contact,
                 recover_rate,
                 birth_death_rate):
        # validate it
        self.total_people = total_people
        self.initial_susceptible_people = initial_susceptible_people
        self.initial_infected_people = initial_infected_people
        self.initial_recovered_people = initial_recovered_people
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


class SirModel:
    def __init__(self, initial_conditions):
        self.init_cond = initial_conditions
        self.sir0 = [self.init_cond.n1(), self.init_cond.n2(), self.init_cond.n3()]

    def __sir_classic(self, sir, t):
        s = sir[0]
        i = sir[1]
        r = sir[2]
        dsdt = -self.init_cond.beta_tilde() * s * i
        didt = (self.init_cond.beta_tilde() * s - self.init_cond.gamma()) * i
        drdt = self.init_cond.gamma() * i
        return [dsdt, didt, drdt]

    def __sir_vital_dynamics(self, sir, t):
        s = sir[0]
        i = sir[1]
        r = sir[2]
        dsdt = -self.init_cond.beta_tilde() * s * i + self.init_cond.d() * (self.init_cond.n() - s)
        didt = (self.init_cond.beta_tilde() * s - self.init_cond.gamma() - self.init_cond.d()) * i
        drdt = self.init_cond.gamma() * i - self.init_cond.d() * r
        return [dsdt, didt, drdt]

    def solve_classic(self, time_linspace):
        return odeint(self.__sir_classic, self.sir0, time_linspace)

    def solve_vital_dynamics(self, time_linspace):
        return odeint(self.__sir_vital_dynamics, self.sir0, time_linspace)


# example
init_cond = InitialConditions(100000, 99900, 10, 90, 5, 0.1, 0.2, 0.02)
model = SirModel(init_cond)
time_linspace = np.linspace(0, 365, 10000)
sir_classic = model.solve_classic(time_linspace)
sir_with_vital_dynamics = model.solve_vital_dynamics(time_linspace)

for i in range(3):
    plt.plot(time_linspace, sir_with_vital_dynamics[:, i])
    # plt.xlim(0, 100)
    # plt.ylim(0, 10000)
    plt.xlabel('time')
    plt.ylabel('i = ' + str(i))
    plt.grid(True)
    plt.title('SIR model with vital dynamics. S(i = 0), I(i = 1), R(i = 2)')
    plt.show()
