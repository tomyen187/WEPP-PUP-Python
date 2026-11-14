The WEPP-PUP tool was implemented in the Python 3.10.2 programming language and operates in standard desktop computing environments.  All simulations presented in this study were conducted on a Windows-based (Windows 11 OS) system using the publicly available WEPP executable (wepp_2012.exe).  The workflow requires standard WEPP input files (weather, soil, slope, and management) and a user-defined parameter configuration file. WEPP-PUP adopts the default WEPP simulation structure and utilizes the standard WEPP input files without modification. Users interested in developing or modifying WEPP input files are referred to the WEPP User Summary (NSERL Report No. 11, July 1995) (https://www.ars.usda.gov/midwest-area/west-lafayette-in/national-soil-erosion-research/docs/wepp/wepp-model-documentation/), which provides detailed guidance on the preparation and formatting of WEPP input datasets.  For typical hillslope applications, complete WEPP-PUP simulations required less than three hours of runtime for 1,000 iterations. 

(The results presented are representative results for demonstration purpose)

-- Open WEPP_PUP_Hill/Single_Variate/04_WEPP folder and install wepp_2012.exe or wepp_2024.exe application

-- Once the WEPP model is installed try installing Python 3.10.2 or greater version and the following libraries

	Libraries: os, NumPy (Version 2.2.6), Matplotlib (Version 3.10.8), subprocess, Pandas (Version 2.3.3), shutil, and math

-- Now the WEPP-PUP is set to work. Now run,
   
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

WEPP-PUP uses stochastic sampling in DDS and PRS parameter searches and in the weather-input perturbation procedure. The current implementation does not prescribe a fixed random seed. Consequently, independent executions may generate different parameter combinations and optimization trajectories, even when the same input data and calibration settings are used.

Users who require repeatable random sampling may explicitly initialize the Python `random` and NumPy `np.random` generators before starting the calibration. For example, `random.seed(42)` and `np.random.seed(42)` can be specified in `main.py`, with the necessary modules imported.

The choice of seed does not change the mathematical formulation of DDS or PRS but determines the pseudorandom sequence generated during a run. For reproducible comparisons, users should also retain the calibration settings, input files, software revision, and resulting outputs. The outputs supplied with the repository document the representative demonstrations reported in this study.
