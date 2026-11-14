# WEPP-PUP example configurations

## No new configuration format is necessary

The existing code reads its main settings directly from `main.py` and the parameter file `WEPP_PUP_cal_param.txt`. Creating a JSON/YAML file without changing the program would **not** affect a run. For the reviewer, these existing files should be documented as the example configurations.

## Exact locations

| Role | Single-variate example | Multivariate example |
|---|---|---|
| Run settings | `WEPP_PUP_Hill/Single_Variate/01_Code/main.py` | `WEPP_PUP_Hill/Multi_Variate/01_Code/main.py` |
| Parameter selection and bounds | `WEPP_PUP_Hill/Single_Variate/03_Parameter/WEPP_PUP_cal_param.txt` | `WEPP_PUP_Hill/Multi_Variate/03_Parameter/WEPP_PUP_cal_param.txt` |
| WEPP run settings | `WEPP_PUP_Hill/Single_Variate/02_Input_Files/p0.run` | `WEPP_PUP_Hill/Multi_Variate/02_Input_Files/p0.run` |
| Weather, soil, slope, management | `.cli`, `.sol`, `.slp`, `.man` in the case's `02_Input_Files` | Same files in the multivariate `02_Input_Files` |
| Reference data | `continuous_observed_runoff.txt` | `cont_obs_runoff_Mul_var.txt` and `cont_obs_sed_Mul_var.txt` |
| Generated outputs | `06_Output/` and `07_Plots/` | `06_Output/` and `07_Plots/` |

## Settings in current example main.py scripts

| Setting | Single variate | Multivariate | Notes |
|---|---|---|---|
| `max_iterations` | `1000` | `1000` | Prescribed evaluation budget |
| `optimization` | `0` | `0` | 0=DDS; 1=PRS |
| `ip_flag` | `0` | `0` | 0=weather perturbation disabled; 1=enabled |
| `MU_index` | `0` | `0` | 0=PER disabled; 1=enabled |
| `restart_flag` | `0` | `0` | 0=fresh start; 1=restart using saved records |
| `calibration_start` | `1963-01-01` | `1995-01-01` | Date in current script |
| `calibration_end` | `1992-12-31` | `2009-12-31` | Date in current script |
| `wepp_path` | `04_WEPP/wepp_2012.exe` | `04_WEPP/wepp_2012.exe` | Absolute paths in the current script must be updated |
| Fixed random seed | None prescribed | None prescribed | See REPRODUCIBILITY.md |

These values describe the default configurations in the repository. Input-uncertainty or PER scenarios require changing the corresponding flags and (where relevant) parameter-file selection.

## Typical configuration task — single-variate demonstration

1. Navigate to `WEPP_PUP_Hill/Single_Variate/01_Code/main.py`.
2. Set all hard-coded directories to the actual location of `Single_Variate` on the local computer.
3. Set `optimization=0`, `ip_flag=0`, `MU_index=0`, `restart_flag=0`, and `max_iterations=1000` for the stored default demonstration.
4. Review `WEPP_PUP_Hill/Single_Variate/03_Parameter/WEPP_PUP_cal_param.txt`. Its calibration-selection column determines which parameters are updated.
5. Confirm the baseline `p0.run` references the intended climate and output filenames.
6. Run `main.py` from the same `01_Code` directory and inspect `06_Output/`.

## Typical configuration task — multivariate demonstration

1. Navigate to `WEPP_PUP_Hill/Multi_Variate/01_Code/main.py`.
2. Set its absolute paths for the multivariate case, including runoff and sediment reference series.
3. Set `optimization=0`, `ip_flag=0`, `MU_index=0`, `restart_flag=0`, and `max_iterations=1000` for the stored default demonstration.
4. Review its independent parameter file and `p0.run` file.
5. Run `main.py` and inspect `06_Output/compare_runoff.txt`, `06_Output/compare_sediment.txt`, and iteration records.

## Optional seeding — not required by the distributed implementation

When repeatable random draws are needed, users may add these lines near the beginning of **the selected** `01_Code/main.py`, before calling `WEPP_PUP_run`:

```python
import random
import numpy as np

random.seed(42)
np.random.seed(42)
```

The integer 42 is illustrative, **not** an original seed for the published results. If different branches of the code consume different numbers of random draws, matching seeds alone will not guarantee identical sequences across different scenarios. Also save the execution platform, library versions, input data, and complete parameter history.


