import preliz as pz
import matplotlib.pyplot as plt
import numpy as np
import arviz_plots as azp

az.style.use("arviz-variat")

def one_iter(lower, upper, mode, mass=0.99, plot=True):

    dist = pz.Beta()
    dist._fit_moments(  # pylint:disable=protected-access
        mean=(upper+lower)/2, 
        sigma=((upper - lower) / 4) / mass
    )
    tau_a = (dist.alpha - 1) / mode
    tau_b = (dist.beta - 1) / (1-mode)
    tau = (tau_a + tau_b) / 2
    prob = dist.cdf(upper) - dist.cdf(lower)

    while abs(prob - mass) > 0.005:

        alpha = 1 + mode * tau
        beta = 1 + (1 - mode) * tau

        dist._parametrization(alpha, beta)
        prob = dist.cdf(upper) - dist.cdf(lower)
        if prob < mass:
            tau += 0.1
        else:
            tau -= 0.1


    if plot:
        dist.plot_pdf(legend=None, color="0.5", alpha=0.5)
    return dist

lower = 0.1
upper = 0.7
prob = 0.90
mode = 0.5

_, ax = plt.subplots(figsize=(10, 4))
dist_ = pz.Beta()

for mode in np.arange(0.15, 0.66, 0.01):
    dist = one_iter(lower, upper, mode=mode, mass=prob)
    vals = dist.xvals("full")
    ax.plot(mode, np.max(dist.pdf(vals)), ".", color="0.5")
pz.maxent(dist_, lower, upper, prob, plot_kwargs={"legend":"None", "color":"C1"});
for line in ax.get_lines()[::3]:
    line.remove()
ax.get_lines()[-2].set_linewidth(2)

plt.savefig("../img/beta_bounds.png")