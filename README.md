The WEPP-PUP tool was implemented in the Python 3.10.2 programming language and operates in standard desktop computing environments.  All simulations presented in this study were conducted on a Windows-based (Windows 11 OS) system using the publicly available WEPP executable (wepp_2012.exe).  The workflow requires standard WEPP input files (weather, soil, slope, and management) and a user-defined parameter configuration file. WEPP-PUP adopts the default WEPP simulation structure and utilizes the standard WEPP input files without modification. Users interested in developing or modifying WEPP input files are referred to the WEPP User Summary (NSERL Report No. 11, July 1995), which provides detailed guidance on the preparation and formatting of WEPP input datasets.  For typical hillslope applications, complete WEPP-PUP simulations required less than three hours of runtime for 1,000 iterations. 


-- Open 04_WEPP folder and install wepp.exe application

-- Once the WEPP model is installed try installing Python 3.10.2 or greater version and the following libraries

	Libraries: os, NumPy (Version 2.2.6), Matplotlib (Version 3.10.8), subprocess, Pandas (Version 2.3.3), shutil, and math

-- Now the WEPP-PUP is set to work.
   
      for single variate application : ...\WEPP_PUP_HILL\Single_variate\01_Code\main.py
      for multivariate application   : ...\WEPP_PUP_HILL\Multi_variate\01_Code\main.py
