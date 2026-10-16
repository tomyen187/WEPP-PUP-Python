
import os
import numpy as np
import pandas as pd
import random
import re

def find_cli_header(lines):
    for i, line in enumerate(lines):
        # Normalize spacing and lowercase
        clean_line = re.sub(r"\s+", " ", line.strip().lower())
        if clean_line.startswith("da mo year prcp"):
            return i
    raise ValueError("no header found starting with da mo year ...")

def IP_uncertainty(iteration, run_file_name, cli_file, parameters, working_folder,ip_flag):


    if not ip_flag:
        # No change, just return original cli path
        return os.path.join(working_folder, cli_file)

    # --- Extract sigma and nu from parameter list ---

    sigma_params = [p for p in parameters if p['variable'].lower() == "sigma" and p['Cal_index'] == 1]
    nu_params = [p for p in parameters if p['variable'].lower() == "nu" and p['Cal_index'] == 1]

    if not sigma_params or not nu_params:
        #print("ℹ️ No input uncertainty (sigma/nu not active in cal_param.txt). Skipping .cli modification.")
        return os.path.join(working_folder, cli_file)  # use original file


    sigma_param = sigma_params[0]
    nu_param = nu_params[0]

    # Get bounds
    sigma_L, sigma_U = sigma_param['lower'], sigma_param['upper']
    nu_L, nu_U  = nu_param['lower'], nu_param['upper']
    sigma_val = np.random.uniform(sigma_L, sigma_U)	
    nu_val    = np.random.uniform(nu_L,nu_U)

    LV= random.gauss(nu_val, sigma_val)


# --------save
    latent_var_file=os.path.join(working_folder,"latent_variable.txt")

    with open(latent_var_file,"w") as f:
        f.write("Iteration\tnu_value\tsigma_value\tL_V\n")

    # Lists to track values for plotting
    iteration, nu_value, sigma_value, L_V = [], [], [], []
    iteration.append(iteration)
    nu_value.append(nu_val)
    sigma_value.append(sigma_val)
    L_V.append(LV)
    
#--------makes new *.cli file for IP_Uncert------

    cli_path = os.path.join(working_folder, cli_file)
    cli_new_file = os.path.join(
        working_folder,
        os.path.splitext(cli_file)[0] + "_1.cli"
    )

    run_path = os.path.join(working_folder, run_file_name)
    with open(run_path, 'r') as f:
        lines = f.readlines()

    with open(run_path, 'w') as f:
        for line in lines:
            if "p0.cli" in line.lower():  					# Look for the default precipitation file name
            
                line = line.replace("p0.cli", os.path.basename(cli_new_file))	# Replace it with the new generated cli file
            f.write(line)

           

# --------read *.cli file (line indices: 0-based)

    with open(cli_file, 'r') as f:
        lines = f.readlines()

    header_block= lines[:15]		#1-15th 
    column_header= lines[13]		#14th line
    data_lines= lines[15:]		#16th line



    data = []
    for line in data_lines:
        parts = line.strip().split()

        if len(parts) < 4:
            data.append(line)  # keep unchanged
            continue

        try:
            prcp = float(parts[3])
        except (IndexError, ValueError):
            data.append(line)
            continue

        new_prcp = LV * prcp
        if new_prcp < 0:
            new_prcp = 0.0

        parts[3] = f"{new_prcp:.2f}"  # format width for alignment
        new_line = "{:>3s}{:>4s}{:>5s}{:>7s}{:>6s}{:>6s}{:>7s}{:>6s}{:>6s}{:>6s}{:>6s}{:>6s}{:>7s}".format(*parts)
        data.append(new_line + "\n")


    with open(cli_new_file, "w") as f:
        f.writelines(header_block)
        f.writelines(data)

    #print(f"✅ New precipitation file created: {cli_new_file}")

    return cli_new_file



  





































