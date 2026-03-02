import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import preliz as pz
from flexitext import flexitext
import arviz_plots as azp


az.style.use("arviz-variat")

_, ax = plt.subplots(1, 1, figsize=(12, 4))

pz.Normal(0, 10).plot_cdf(ax=ax, legend=None)
pz.Normal(0, 1.3).plot_cdf(ax=ax, legend=None)
pz.Normal(0, 3.6).plot_cdf(ax=ax, legend=None)


for line in ax.get_lines():
    line.set_linewidth(3)


alpha = 0.001
for i in np.linspace(-6, 0, 150):
    ax.fill_between([-i, i], -0.3, 1.3, alpha=alpha, color="0.5")
    alpha += 0.0001

ax.legend([mpatches.Patch(color="0.75")], 
          ["as-yet unobserved data"])


ax.set_ylim(-0.01, 1.01)
ax.set_xticks([])
ax.set_xlabel("observable data")

# Add flexitext
text = ("<size:18> Prior predictive distributions induced by\n"
        "<color:C0, weight:bold>vague</>, <color:C1, weight:bold>informative</>, and <color:C2, weight:bold>weakly informative </>priors</>")
flexitext(0.27, 1.02, text, va="bottom", ma="center", xycoords="figure fraction");

plt.savefig("../img/prior_vagueness.png")