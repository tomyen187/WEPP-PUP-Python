WEPP-PUP (Water Erosion Prediction Project – Parameter estimation and Uncertainty analysis Program) is a Python workflow for repeated execution and calibration of the WEPP hillslope model. The current repository contains separate **single-variate** (runoff) and **multivariate** (runoff and sediment yield) examples. The framework automates parameter updates, execution of WEPP, objective-function evaluation, and saving of iteration-level results. It includes options for weather-input perturbation and Probable Error Range (PER)-based evaluation.


The WEPP-PUP tool was implemented in the Python 3.10.2 programming language and operates in standard desktop computing environments.  All simulations presented in this study were conducted on a Windows-based (Windows 11 OS) system using the publicly available WEPP executable (wepp_2012.exe).  The workflow requires standard WEPP input files (weather, soil, slope, and management) and a user-defined parameter configuration file. WEPP-PUP adopts the default WEPP simulation structure and utilizes the standard WEPP input files without modification. Users interested in developing or modifying WEPP input files are referred to the WEPP User Summary (NSERL Report No. 11, July 1995) (https://www.ars.usda.gov/midwest-area/west-lafayette-in/national-soil-erosion-research/docs/wepp/wepp-model-documentation/), which provides detailed guidance on the preparation and formatting of WEPP input datasets.  For typical hillslope applications, complete WEPP-PUP simulations required less than three hours of runtime for 1,000 iterations. 

(The results presented are representative results for demonstration purpose)

-- Open WEPP_PUP_Hill/Single_Variate/04_WEPP folder and install wepp_2012.exe or wepp_2024.exe application

-- Once the WEPP model is installed try installing Python 3.10.2 or greater version and the following libraries

	Libraries: os, NumPy (Version 2.2.6), Matplotlib (Version 3.10.8), subprocess, Pandas (Version 2.3.3), shutil, and math

	Standard-library modules such as `os`, `subprocess`, `shutil`, `math`, and `random` do not require separate `pip` installation. See [requirements.txt](requirements.txt) for the declared third-party dependencies; these versions are transcribed from the existing README and **still require a clean-environment installation test** before being presented as a validated lockfile.

Install the Python dependencies from the repository root:

```powershell
py -m pip install -r requirements.txt
```


## Existing repository structure

```text
WEPP_PUP_Hill/
├── Single_Variate/
│   ├── 01_Code/                # main.py, DDS/PRS, file update, objective function
│   ├── 02_Input_Files/         # .cli, .sol, .slp, .man, .run, runoff reference series
│   ├── 03_Parameter/           # WEPP_PUP_cal_param.txt
│   ├── 04_WEPP/                # WEPP executables and batch files
│   ├── 05_Working_Inputs/      # generated working copies
│   ├── 06_Output/              # saved iteration results, WEPP outputs, diagnostic plots
│   ├── 07_Plots/               # additional saved diagnostic plots
│   └── 08_Post_Process/        # post-processing script and validation workbook
└── Multi_Variate/
    └── [same numbered directory structure, with runoff and sediment-yield files]
```

Both existing `01_Code/main.py` files are the **actual run configuration scripts**. `03_Parameter/WEPP_PUP_cal_param.txt` contains the parameter-level configuration. The WEPP `.run` and associated input files provide the WEPP model setup. No additional YAML or JSON configuration file is required by the current program. See (CONFIGURATION_GUIDE.md).

## Running the demonstration

1. Download or clone the repository and choose `Single_Variate` or `Multi_Variate`.
2. Open the selected case's `01_Code/main.py` and replace its example `V:\acerlaptop\...` paths with absolute paths valid on your Windows computer. **Do not change the names of the numbered folders without also updating path references.**
3. Check that `04_WEPP/wepp_2012.exe` is available and that the `p0.run` file references the intended input and output locations.
4. Open `03_Parameter/WEPP_PUP_cal_param.txt` and check parameter selection, initial values, and parameter bounds.
5. Review `max_iterations`, `optimization`, `ip_flag`, `MU_index`, `restart_flag`, and the calibration period in `01_Code/main.py`.

6. Now the WEPP-PUP is set to work. Now run the main.py for execution of code.
   
      for single variate application : ...\WEPP_PUP_HILL\Single_variate\01_Code\main.py
      for multivariate application   : ...\WEPP_PUP_HILL\Multi_variate\01_Code\main.py


### Example configurations and simulation outputs

The repository contains separate examples for single-variate and multivariate WEPP calibration under the `WEPP_PUP_Hill` directory.

For each application, `01_Code/main.py` contains the main simulation settings, including the optimization method, number of iterations, uncertainty options, calibration period, and input and output paths. The parameter file `03_Parameter/WEPP_PUP_cal_param.txt` specifies the parameters selected for calibration, their initial values, and their permissible ranges.

The `02_Input_Files` directory contains the WEPP input datasets and reference series used in the demonstration. The corresponding simulation outputs, calibration records, and diagnostic plots are provided in `06_Output` and `07_Plots`.

Before running the program, users should update the file paths in `main.py` to match their local directory structure and verify the paths referenced in the WEPP `.run` file. The examples use the WEPP 2012 executable, as described in the manuscript.


-- Note: Make sure if any changes are made to the folder name (ex. output) that should be reflected in p0.run from 02_Input_Files folder
		Open p0.run file and modify the lines: ..\06_Output\evbe_1.txt :  provide the updated folder name


### Random sampling and reproducibility

Regarding random seeds, we would like to clarify that the DDS algorithm follows a stochastic search procedure, as originally described by Tolson and Shoemaker (2007). In DDS, random numbers are used to select the parameter dimensions to be perturbed and to determine the magnitude of those perturbations. The random seed serves as an initialization value for the pseudorandom-number generator rather than as a fixed parameter prescribed by the DDS algorithm.

In the present WEPP-PUP implementation, DDS and PRS use Python's pseudorandom-number generator, while the weather-input perturbation routine uses random draws from both Python and NumPy. A fixed random seed was not prescribed for the representative calibration experiments. Consequently, independent executions may produce different optimization trajectories and retained parameter combinations, even when the parameter bounds, objective functions, and model inputs remain unchanged.

We acknowledge that specifying a fixed seed is useful when exact repetition of an individual stochastic search is required. However, introducing a seed retrospectively would not reconstruct the random-number sequences used in the original experiments. We have therefore retained the existing initialization procedure for the present study and clarified this implementation choice in the manuscript. Users requiring repeatable runs may explicitly initialize the Python and NumPy random-number generators before executing WEPP-PUP, without modifying the underlying DDS or PRS algorithms.

Users who require repeatable random sampling may explicitly initialize the Python `random` and NumPy `np.random` generators before starting the calibration. For example, `random.seed(42)` and `np.random.seed(42)` can be specified in `main.py`, with the necessary modules imported.

The choice of seed does not change the mathematical formulation of DDS or PRS but determines the pseudorandom sequence generated during a run. For reproducible comparisons, users should also retain the calibration settings, input files, software revision, and resulting outputs. The outputs supplied with the repository document the representative demonstrations reported in this study.
A user who needs repeatable random sampling may optionally insert the following **before** the WEPP-PUP run in the selected `01_Code/main.py`:

```python
import random
import numpy as np

user_seed = 42  # illustrative; not claimed to have generated published figures
random.seed(user_seed)
np.random.seed(user_seed)
```


Reference:
Tolson, B.A. and C.A. Shoemaker, 2007. Dynamically Dimensioned Search Algorithm for Computationally Efficient Watershed Model Calibration. Water Resources Research 43: W01413, DOI: 10.1029/2005WR004723.


