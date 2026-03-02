import numpy as np
from scipy.optimize import minimize
from scipy.stats import entropy
import matplotlib.pyplot as plt
import arviz_plots as azp

az.style.use("arviz-variat")

cons = [[{"type": "eq", "fun": lambda x: np.sum(x) - 1}],
        [{"type": "eq", "fun": lambda x: np.sum(x) - 1},
         {"type": "eq", "fun": lambda x: 30 - np.sum(x * np.arange(0, 120))}],
        [{"type": "eq", "fun": lambda x: np.sum(x) - 1},
         {"type": "eq", "fun": lambda x: np.sum(x[range(60, 90)]) - 0.70}]]

_, axes = plt.subplots(1, 3, figsize=(10, 3), sharey=True, constrained_layout=True)

titles = ["No constraints",
          "Mean=0.25",
          "70% of the mass\n between 0.5-0.75"]

for i, (c, ax, title) in enumerate(zip(cons, axes, titles)):    
    val = minimize(lambda x: -entropy(x), 
                   x0=[1/120]*120,
                   tol=1e-8,
                   constraints=c)['x']
    

    ax.plot(np.linspace(0, 1, 120), val, color=f"C{i}", lw=3)
    ax.set_yticks([])
    ax.set_title(title)
    ax.axhline(0, color="0.75", ls="--", lw=1)

plt.savefig("../img/max_ent.png")