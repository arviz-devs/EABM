import arviz_plots as azp
import numpy as np
import preliz as pz
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
az.style.use("arviz-variat")

np.random.seed(123)

fig, ax = plt.subplots(1, 1, figsize=(8, 3))

y_lim = 75
n_trials = list(range(0, 100, 5))
n_trials.extend(range(100, 1000, 50))
n_trials.extend(range(1000, 10000, 1000))
success = [pz.Binomial(n, 0.34).rvs() for n in n_trials]

last_trial = n_trials[-1]
last_success = success[-1]

for i in range(20):
    n_trials.insert(0, 0)
    success.insert(0, 0)

for i in range(25):
    n_trials.append(last_trial)
    success.append(last_success)

beta_params = [(0.5, 0.5), (10, 10)]
θ = np.linspace(0, 1, 5000)

N = n_trials[0]
y = success[0]

for jdx, (a_prior, b_prior) in enumerate(beta_params):
    p_theta_given_y = pz.Beta(a_prior + y, b_prior + N - y).pdf(θ)
    ax.plot(θ, p_theta_given_y, lw=4)

ax.set_yticks([])
ax.set_ylim(0, y_lim)
ax.set_title(f'{N:4d} trial {y:4d} success')

plt.savefig("../img/beta_binomial_update.png")


def update(idx):
    ax.clear()
    ax.set_xlabel(r'$\theta$')
    ax.set_yticks([])
    ax.set_ylim(0, y_lim)

    N = n_trials[idx]
    y = success[idx]
    s_n = ('s' if (N > 1) else '')

    for a_prior, b_prior in beta_params:
        p_theta_given_y = pz.Beta(a_prior + y, b_prior + N - y).pdf(θ)
        ax.plot(θ, p_theta_given_y, lw=4)

        ax.set_title(f'{N:4d} trial{s_n} {y:4d} success')



ani = FuncAnimation(fig, update, frames=len(n_trials), interval=125, repeat=False)
ani.save("../img/beta_binomial_update.gif")