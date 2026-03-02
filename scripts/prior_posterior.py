import arviz_plots as azp
import numpy as np
import preliz as pz
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

az.style.use("arviz-variat")
fig, ax = plt.subplots(1, 1, figsize=(8, 2.5))

grid = np.linspace(0, 1, 500)

likelihood = pz.Binomial(192, grid).pdf(96)
likelihood /= likelihood.sum()

alphas_0 = list(range(2, 40))
alphas_1 = list(range(1, 40))

alphas = alphas_0 + alphas_1
betas = alphas_0[::-1] + alphas_1


def update(idx):
    ax.clear()

    prior = pz.Beta(alphas[idx], betas[idx]).pdf(grid)
    posterior = likelihood * prior
    prior /= prior.sum()
    posterior /= posterior.sum()

    ax.plot(grid, likelihood, '-', label="likelihood", color="k", lw=1)
    ax.plot(grid, prior, '-', label="prior", color="C0", lw=1)
    ax.plot(grid, posterior, '-', label="posterior", color="C0", lw=4)

    ax.set_yticks([])
    ax.set_ylim(0, 0.035)
    ax.legend(loc="upper right", fontsize=9)

ani = FuncAnimation(fig, update, frames=len(alphas), interval=150, repeat=False)
ani.save("../img/prior_posterior.gif")