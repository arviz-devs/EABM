import arviz_plots as azp
import numpy as np
import preliz as pz
import matplotlib.pyplot as plt

az.style.use("arviz-variat")

grid = np.linspace(0, 1, 500)
prior = pz.Beta(4, 8).pdf(grid)
likelihood = pz.Binomial(36, grid).pdf(24)
posterior = likelihood * prior
prior /= prior.sum()
likelihood /= likelihood.sum()
posterior /= posterior.sum()
_, ax = plt.subplots(sharex=True, figsize=(8, 3))
ax.plot(grid, prior, '-', label="prior", lw=2)
ax.plot(grid, likelihood, '-', label="likelihood", lw=2)
ax.plot(grid, posterior, '-', label="posterior", lw=3)

ax.set_xticks([])
ax.set_yticks([])
ax.legend()
plt.savefig("../img/bayes_theorem_00.png")


_, ax = plt.subplots(2, 1, sharex=True,  sharey=True, figsize=(8, 3))

prior_trunc = prior.copy()
prior_trunc[320:] = 0
posterior_trunc = likelihood * prior_trunc
prior_trunc /= prior_trunc.sum()
posterior_trunc /= posterior_trunc.sum()

ax[0].plot(grid, prior, '-', label="prior", lw=2)
ax[0].plot(grid, likelihood, '-', label="likelihood", lw=2)
ax[0].plot(grid, posterior, '-', label="posterior", lw=3)

ax[1].plot(grid, prior_trunc, '-', label="prior", lw=2)
ax[1].plot(grid, likelihood, '-', label="likelihood", lw=2)
ax[1].plot(grid, posterior_trunc, '-', label="posterior", lw=3)

ax[0].axvline(320/500,0, 1, ls="--", color="0.5")
ax[1].axvline(320/500,0, 1, ls="--", color="0.5")

ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].legend()
plt.savefig("../img/bayes_theorem_01.png")
