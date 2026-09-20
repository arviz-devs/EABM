import numpy as np
import pandas as pd
import xarray as xr
import pymc as pm
from pathlib import Path

SEED = 5838296
P = 4
L = 20
OUTPUT_DIR = Path(__file__).parent.parent / "prerun"

lake_huron = pd.read_csv("../../data/lake_huron.csv")
y = lake_huron["value"].to_numpy()
N = len(y)
lags = np.column_stack([y[P - k:N - k] for k in range(1, P + 1)])

coords = {"lag": np.arange(1, P + 1), "time": np.arange(P, N)}

with pm.Model(coords=coords) as ar_model:
    lag_data = pm.Data("lags", lags, dims=("time", "lag"))
    y_data = pm.Data("y_obs", y[P:], dims="time")
    mu = pm.StudentT("mu", nu=3, mu=np.median(y), sigma=2.5)
    rho = pm.Normal("rho", mu=0, sigma=0.5, dims="lag")
    sigma = pm.HalfStudentT("sigma", nu=3, sigma=2.5)
    mean = mu + pm.math.dot(lag_data - mu, rho)
    pm.Normal("y", mu=mean, sigma=sigma, observed=y_data, dims="time")


def fit_ar(cutoff):
    """Fit the AR(4) model to the first cutoff observations."""
    with ar_model:
        pm.set_data(
            {"lags": lags[:cutoff - P], "y_obs": y[P:cutoff]},
            coords={"time": np.arange(P, cutoff)},
        )
        return pm.sample(
            draws=1000,
            tune=1000,
            chains=4,
            target_accept=0.99,
            random_seed=SEED + cutoff,
            progressbar=False
        )


# Full fit with the pointwise log-likelihood used by loo and lfo_cv
idata = fit_ar(N)
with ar_model:
    pm.compute_log_likelihood(idata, progressbar=False)
idata.to_netcdf(OUTPUT_DIR / "lfo_cv_00.nc")

# Posterior draws for every training window that exact and approximate LFO-CV can request
cutoffs = np.arange(L, N + 1)
posteriors = [fit_ar(int(cutoff)).posterior.ds[["mu", "rho", "sigma"]] for cutoff in cutoffs]
refits = xr.concat(posteriors, dim=pd.Index(cutoffs, name="cutoff"))
refits.to_netcdf(OUTPUT_DIR / "lfo_cv_01.nc")
