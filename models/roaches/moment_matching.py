import numpy as np
import pandas as pd
import bambi as bmb
from pathlib import Path

SEED = 4711
OUTPUT_DIR = Path(__file__).parent.parent / "prerun"

roaches = pd.read_csv("../../data/roaches.csv", index_col=0)
roaches['log_exposure2'] = np.log(roaches['exposure2'])

model = bmb.Model(
    'y ~ roach1 + treatment + senior + offset(log_exposure2)',
    data=roaches,
    family='poisson',
    priors={
        'roach1': bmb.Prior('Normal', mu=0, sigma=2.5),
        'treatment': bmb.Prior('Normal', mu=0, sigma=2.5),
        'senior': bmb.Prior('Normal', mu=0, sigma=2.5),
        'Intercept': bmb.Prior('Normal', mu=0, sigma=5.0)
    }
)

idata = model.fit(
    draws=1000,
    tune=1000,
    chains=4,
    random_seed=SEED,
    idata_kwargs={'log_likelihood': True}
)

output_path = OUTPUT_DIR / "moment_matching_00.nc"
idata.to_netcdf(output_path)
