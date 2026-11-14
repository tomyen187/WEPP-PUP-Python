# Reproducibility statement for WEPP-PUP

## What the current repository makes available

The public repository contains the Python calibration framework; separate hillslope single-variate and multivariate applications; benchmark/reference input series; WEPP input files; model and parameter configuration files; and saved model/optimization outputs. These assets permit inspection of the calibration procedure and independent reruns of the demonstration settings, subject to successful installation and correct paths.

## Stochastic choices in the current implementation

| Component | Source file in each case | Random draws | Recorded fixed seed in existing code? |
|---|---|---|---|
| DDS | `01_Code/optimise.py` | `random.random()`, `random.randrange()`, `random.gauss()` | No |
| PRS | `01_Code/PRS.py` | `random.uniform()` | No |
| Precipitation perturbation | `01_Code/IP.py` | `np.random.uniform()` and `random.gauss()` | No |

Python's `random` and NumPy's `np.random` are separate pseudorandom-number systems. A seed is an initial value for a generator; it is **not** a required DDS calibration constant. The DDS perturbation-scale setting (currently `0.2` in `optimise.py`) is conceptually different from an RNG seed.

## Optional user-specified random seed

The current released source has not been modified to force a default seed. A user who wants repeatable stochastic sampling may add the following near the beginning of the selected case's `01_Code/main.py`, before the WEPP-PUP run:

```python
import random
import numpy as np

user_seed = 42     # illustrative only
random.seed(user_seed)
np.random.seed(user_seed)
```

It is not claimed that 42, or any other newly selected seed, generated the archived manuscript results. Exact repetition also depends on preserving the same code revision, Python/package versions, inputs, paths/configuration, execution order and environment.

## What cannot be claimed for the archived experiments

The existing code does not explicitly record the initial RNG state or fixed seed with the supplied output records. Accordingly, the archived trajectories are evidence of the searches that were conducted, but their precise sequences are **not independently recoverable from a newly selected seed**. The presence of a repository, example inputs, and an output archive is different from proof of exact numerical reproduction.

This limitation does not invalidate a stochastic optimization method. It does, however, limit claims that a reader can reproduce the *identical* parameter sequence and objective-function trajectory reported in the manuscript. Interpret iteration counts as properties of the archived searches, not deterministic convergence guarantees.




## Provenance needed for a fully reproducible demonstration

For each run, retain: the exact Git commit or release tag; `main.py` settings; parameter configuration file; WEPP `.run`, `.cli`, `.sol`, `.slp` and `.man` files; observed/reference series; selected executable and version; Python and dependency versions; operating system; output files; and either the random seed/initial state or the complete original parameter and objective-function history.


