import numpy as np
import pandas as pd
import pymc as pm
import xarray as xr
import arviz.preview as azp
from pymc_extras import fit_laplace
import lzma
from pathlib import Path

SEED = 4711

def compress(nc_path, threshold_mb=50):
    nc_file = Path(nc_path)
    if not nc_file.exists():
        return

    size_mb = nc_file.stat().st_size / (1024 * 1024)
    if size_mb > threshold_mb:
        xz_file = Path(str(nc_path) + ".xz")
        with open(nc_file, "rb") as f_in:
            with lzma.open(xz_file, "wb", preset=9) as f_out:
                f_out.write(f_in.read())
        nc_file.unlink()

wells = pd.read_csv("./data/wells.csv")
wells["dist100"] = wells["dist"] / 100

X = np.column_stack([
    np.ones(len(wells)),
    wells["dist100"].values,
    wells["arsenic"].values
])
y = wells["switch"].values

with pm.Model():
    beta = pm.Normal("beta", mu=0, sigma=1, shape=3)
    logit_p = pm.math.dot(X, beta)
    pm.Bernoulli("y", logit_p=logit_p, observed=y)

    idata = pm.sample(
        draws=1000,
        tune=1000,
        chains=4,
        random_seed=SEED,
        progressbar=True,
        idata_kwargs={"log_likelihood": True}
    )

data = azp.convert_to_datatree(idata)
data["constant_data"] = xr.Dataset({"X": (["obs_id", "coef"], X)})
data.to_netcdf("models/prerun/model_comparison_large_data_00.nc")
compress("models/prerun/model_comparison_large_data_00.nc")

with pm.Model() as model_laplace:
    beta = pm.Normal("beta", mu=0, sigma=1, shape=3)
    logit_p = pm.math.dot(X, beta)
    pm.Bernoulli("y", logit_p=logit_p, observed=y)

    idata_laplace = fit_laplace(
        chains=4,
        draws=2000,
        random_seed=SEED,
        progressbar=True
    )

idata_laplace.to_netcdf("models/prerun/model_comparison_large_data_01.nc")
compress("models/prerun/model_comparison_large_data_01.nc")

data_laplace = azp.convert_to_datatree(idata_laplace)
data_laplace["observed_data"] = xr.Dataset({
    "y": (["obs_id"], y, {"obs_id": range(len(y))})
})
data_laplace["constant_data"] = xr.Dataset({"X": (["obs_id", "coef"], X)})
data_laplace.to_netcdf("models/prerun/model_comparison_large_data_02.nc")
compress("models/prerun/model_comparison_large_data_02.nc")

X_log = X.copy()
X_log[:, 2] = np.log(X[:, 2])

with pm.Model():
    beta2 = pm.Normal("beta", mu=0, sigma=1, shape=3)
    logit_p2 = pm.math.dot(X_log, beta2)
    pm.Bernoulli("y", logit_p=logit_p2, observed=y)

    idata2 = pm.sample(
        draws=1000,
        tune=1000,
        chains=4,
        random_seed=SEED,
        progressbar=True,
        idata_kwargs={"log_likelihood": True}
    )

data2 = azp.convert_to_datatree(idata2)
data2["constant_data"] = xr.Dataset({"X": (["obs_id", "coef"], X_log)})
data2.to_netcdf("models/prerun/model_comparison_large_data_03.nc")
compress("models/prerun/model_comparison_large_data_03.nc")
