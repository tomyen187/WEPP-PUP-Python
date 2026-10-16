import os
import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from MU import compute_uncertainty
import stats as st

#=======================read files func. =================================================
def read_observed_runoff(Obs_path):
    obs_dates=[]
    obs_val=[]
    obs_data = []
    with open(Obs_path, 'r') as f:
        next(f)
        for line in (f):
            data = line.strip().split()			#[float(line.strip().split()[-1]) for line in f if line.strip()]
            year =int(data[0])
            month = int(data[1])
            day= int(data[2])
            obs_runoff = float(data[3])
            date = datetime(year, month, day)
        
            obs_dates.append(date)
            obs_val.append(obs_runoff)
            obs_data.append(data)
 
    return obs_dates, obs_val,obs_data


def read_model_output(out_path):
    sim_date=[]
    sim_values=[]
    sim_data = []
    with open(out_path, 'r') as f:
        for _ in range(3):
            next(f)

        for line in (f):
            if not line.strip():			# Skip empty lines
                continue

            data = line.strip().split()			# Split the line into components
            year =int(data[2])
            month = int(data[1])
            day= int(data[0])
            sim_runoff = float(data[4])

            date = datetime(year, month, day)
            sim_date.append(date)
            sim_values.append(sim_runoff)
            sim_data.append(data)


    return sim_date, sim_values, sim_data




#=======================Obj_func. =================================================
def objective_function(output_folder, Obs_path, out_path, compare_file,iteration, MU_index,calibration_start, calibration_end):

   # Read observed data
    obs_data = []
    with open(Obs_path, 'r') as obs_f:
        next(obs_f)  # skip header
        for line in obs_f:
            if not line.strip():
                continue
            parts = line.strip().split()
            year, month, day, runoff = int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3])
            obs_data.append({
                "Date": datetime(year, month, day),
                "Year_obs": year,
                "Month_obs": month,
                "Day_obs": day,
                "Runoff_obs": runoff
            })


    # Read sim file
    start_year=obs_data[0]["Year_obs"]

    # Keep start_year from the ORIGINAL, unfiltered observation file.
    # Restrict scoring to the requested calibration period.
    calibration_start_date = datetime.strptime(calibration_start, "%Y-%m-%d")
    calibration_end_date = datetime.strptime(calibration_end, "%Y-%m-%d")
    if calibration_start_date > calibration_end_date:
        raise ValueError("calibration_start must not be after calibration_end")
    obs_data = [
        row for row in obs_data
        if calibration_start_date <= row["Date"] <= calibration_end_date
    ]
    if not obs_data:
        raise ValueError("No observation rows fall within the calibration period")

    sim_data = {}
   
    with open(out_path, 'r') as f:
        for _ in range(1,4):
            next(f)

        for line in f:
            parts = line.strip().split()
            if len(parts) < 14:
                continue
            if not parts[0].isdigit():
                continue

            try:
                day, month, year = map(int, parts[:3])
                runoff = float(parts[4])
                #date = datetime(year, month, day)

                wepp_year = int(parts[2])

                actual_year = start_year + (wepp_year - 1)
                date =  datetime(actual_year, month, day)
                sim_data[date] = runoff
            except:
                continue

    # Determine start and end date
    all_dates = sorted(sim_data.keys())
    
    start_date=datetime(start_year, 1,1)
    end_date = datetime(all_dates[-1].year,12,31)

       # --- Merge observed and simulated into one list ---
    combined_rows = []

    obs_dict = {row["Date"]: row for row in obs_data}

    for obs_row in obs_data:  # Loop over all observed dates
        date = obs_row["Date"]
        sim_runoff = sim_data.get(date, -88.00)  # Fill -88 if simulation missing
        combined_rows.append({
            "Year_obs": obs_row["Year_obs"],
            "Month_obs": obs_row["Month_obs"],
            "Day_obs": obs_row["Day_obs"],
            "Runoff_obs": obs_row["Runoff_obs"],
            "Year_sim": date.year,
            "Month_sim": date.month,
            "Day_sim": date.day,
            "Runoff_sim": sim_runoff
        })

    # --- Save to TXT ---
    with open(compare_file, 'w') as f:
        f.write("Yr_obs\tMon_obs\tDay_obs\tRoF_obs\tYr_sim\tMon_sim\tDay_sim\tRoF_sim\n")
        for row in combined_rows:
            
            f.write(f"{row['Year_obs']}\t{row['Month_obs']}\t{row['Day_obs']}\t{row['Runoff_obs']}\t"
                    f"{row['Year_sim']}\t{row['Month_sim']}\t{row['Day_sim']}\t{row['Runoff_sim']}\n")

   # print("✅ Comparison file created successfully (TXT & Excel).")

    valid_obs = []
    valid_sim = []
    for row in combined_rows:
        if row["Runoff_obs"] != -99.00 and row["Runoff_sim"] != -88.00:
            valid_obs.append(row["Runoff_obs"])
            valid_sim.append(row["Runoff_sim"])


    if valid_obs:
        if MU_index == 1: 												#(considering MU by using Probable Error Range (PER))
           obj_func, rmse, corr, nse, pbias  = compute_uncertainty(compare_file, output_folder, iteration)
            
        else:
                
            rmse = st.compute_rmse(valid_sim, valid_obs)
            corr = st.pearson_r(valid_sim, valid_obs)
            nse = st.compute_nse(valid_sim, valid_obs)
            pbias= st.compute_pbias(valid_sim, valid_obs)
           #obj_func = 1-nse+abs(pbias)				# if needed as per application of the study
            obj_func = 1-nse
        print ( f"🟢Obj_func= {obj_func:.4f}",f"NSE= {nse:.4f}",f"PBIAS= {pbias:.4f}",f"RMSE= {rmse:.4f}",f"Corr.Coeff= {corr:.4f}")

      
    return obj_func, rmse, corr, nse, pbias







    


  
  



