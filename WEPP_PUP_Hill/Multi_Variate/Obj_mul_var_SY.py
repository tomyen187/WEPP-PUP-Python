import os
import numpy as np
import pandas as pd
from datetime import datetime
import stats as st  
from MU import compute_uncertainty


# =================Objective Function for Runoff & Sediment ================


def objective_function_Mul(output_folder, Obs_path, sed_obs_path, out_path, runoff_compare_file,sed_compare_file, iteration,  MU_index, calibration_start, calibration_end):

# Read all inputs

    Rof_data = []
    with open(Obs_path, 'r') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
   
            year, month, day, runoff = int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3])
            Rof_data.append({"Date": datetime(year, month, day),"Year_rof": year, "Month_rof": month, "Day_rof": day,"Runoff_obs": runoff})
    

    sed_data = []
    with open(sed_obs_path, 'r') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
   
            year, month, day, sed_obs = int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3])
            sed_data.append({"Date": datetime(year, month, day),"Year": year, "Month": month, "Day": day,"Sed_obs": sed_obs})



    start_year=Rof_data[0]["Year_rof"]



    calibration_start_date = datetime.strptime(calibration_start, "%Y-%m-%d")
    calibration_end_date = datetime.strptime(calibration_end, "%Y-%m-%d")
    if calibration_start_date > calibration_end_date:
        raise ValueError("calibration_start must not be after calibration_end")

    Rof_data = [
        row for row in Rof_data
        if calibration_start_date <= row["Date"] <= calibration_end_date
    ]
    if not Rof_data:
        raise ValueError("No observation rows fall within the calibration period")


    calibration_start_date = datetime.strptime(calibration_start, "%Y-%m-%d")
    calibration_end_date = datetime.strptime(calibration_end, "%Y-%m-%d")
    if calibration_start_date > calibration_end_date:
        raise ValueError("calibration_start must not be after calibration_end")

    sed_data = [
        row for row in sed_data
        if calibration_start_date <= row["Date"] <= calibration_end_date
    ]
    if not sed_data:
        raise ValueError("No observation rows fall within the calibration period")


    
    sim_data = {}
    with open(out_path, 'r') as f:
        for _ in range(1,4):
            next(f)
        
        for line in f:
            parts = line.strip().split()
            if len(parts) < 14:
                continue
            try:
                day, month, wepp_year = map(int,parts[:3])
                runoff = float(parts[4])
                sediment = float(parts[12])


                actual_year = start_year + (wepp_year - 1)
                date =  datetime(actual_year, month, day)
                sim_data[date] = {"Runoff_sim": runoff, "Sed_sim": sediment}
            except:
                continue
            


# ---- Combine Runoff ----


    # Determine start and end date
    all_dates = sorted(sim_data.keys())
    
    start_date=datetime(start_year, 1,1)
    end_date = datetime(all_dates[-1].year,12,31)


   # runoff_compare_file = os.path.join(output_folder, "compare_runoff.txt")

    combined_runoff = []
    
    Rof_dict = {row["Date"]: row for row in Rof_data}


    for obs in  Rof_data:
        date = obs["Date"]
        sim_runoff = sim_data.get(date, {"Runoff_sim": -88})
        combined_runoff.append({
            "date":  obs["Date"],
            "Year_obs": obs["Year_rof"],
            "Month_obs": obs["Month_rof"],
            "Day_obs": obs["Day_rof"],
            "RoF_obs": obs["Runoff_obs"],
            "RoF_sim": sim_runoff["Runoff_sim"]
        })

# Save runoff comparison file
    with open(runoff_compare_file, "w") as f:
        f.write("Yr_obs\tMon_obs\tDay_obs\tRoF_obs\tRoF_sim\n")
        for row in combined_runoff:
            f.write(f"{row['Year_obs']}\t{row['Month_obs']}\t{row['Day_obs']}\t"f"{row['RoF_obs']}\t{row['RoF_sim']}\n")

# ---- Combine Sediment ----
 #   sed_compare_file = os.path.join(output_folder, "compare_sediment.txt")

    combined_sed = []
    sed_dict = {row["Date"]: row for row in sed_data}


    for obs_s in sed_data:
        date = obs_s["Date"]
        sim = sim_data.get(date,{"Sed_sim": -88})
        combined_sed.append({
            "date": obs_s["Date"],
            "Year_obs": obs_s["Year"],
            "Month_obs": obs_s["Month"],
            "Day_obs": obs_s["Day"],
            "Sed_obs": obs_s["Sed_obs"],
            "Sed_sim": sim["Sed_sim"]
        })

# Save sediment comparison file
    with open(sed_compare_file, "w") as f:
        f.write("Yr_obs\tMon_obs\tDay_obs\tSed_obs\tSed_sim\n")
        for row in combined_sed:
            f.write(f"{row['Year_obs']}\t{row['Month_obs']}\t{row['Day_obs']}\t"
                    f"{row['Sed_obs']}\t{row['Sed_sim']}\n")

# ---- Compute Metrics ----
# Runoff
    valid_obs_rof = []
    valid_sim_rof = []
    valid_obs_sed = []
    valid_sim_sed = []

    for row in combined_runoff:
        if row["RoF_obs"] != -99 and row["RoF_sim"] != -88:
            valid_obs_rof.append(row["RoF_obs"])
            valid_sim_rof.append(row["RoF_sim"])

    for r in combined_sed:
        if r["Sed_obs"] != -99 and r["Sed_sim"] != -88:
            valid_obs_sed.append(r["Sed_obs"])
            valid_sim_sed.append(r["Sed_sim"])



# Compute statistics
# ---- Combine and Filter Valid Data for Both Runoff & Sediment ----

    valid_combined = []

    for obs_rof, obs_sed in zip(combined_runoff, combined_sed):
        if obs_rof["date"] == obs_sed["date"]:
            date_str = f"{obs_rof['Year_obs']}-{obs_rof['Month_obs']:02d}-{obs_rof['Day_obs']:02d}"
            rof_obs, rof_sim = obs_rof["RoF_obs"], obs_rof["RoF_sim"]
            sed_obs, sed_sim = obs_sed["Sed_obs"], obs_sed["Sed_sim"]
            if (rof_obs != -99 and rof_sim != -88) and (sed_obs != -99 and sed_sim != -88):
                valid_combined.append({
                    "Date": date_str,
                    "RoF_obs": rof_obs,
                    "RoF_sim": rof_sim,
                    "Sed_obs": sed_obs,
                    "Sed_sim": sed_sim
                })

# ---- Extract Valid Lists ----
    valid_obs_rof = [r["RoF_obs"] for r in valid_combined if r["RoF_obs"] != -99 and r["RoF_sim"] != -88]
    valid_sim_rof = [r["RoF_sim"] for r in valid_combined if r["RoF_obs"] != -99 and r["RoF_sim"] != -88]
    valid_obs_sed = [r["Sed_obs"] for r in valid_combined if r["Sed_obs"] != -99 and r["Sed_sim"] != -88]
    valid_sim_sed = [r["Sed_sim"] for r in valid_combined if r["Sed_obs"] != -99 and r["Sed_sim"] != -88]



    if valid_obs_rof and valid_obs_sed:
        if MU_index == 1: 
            Obj_overall, runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias  = compute_uncertainty(runoff_compare_file, sed_compare_file,output_folder, iteration)



        else:

# ---- Compute Statistics Only When Valid Data Exists ----

            if len(valid_obs_rof) >= 0 and len(valid_obs_sed) >= 0:
                runoff_rmse = st.compute_rmse(valid_sim_rof, valid_obs_rof)
                runoff_corr = st.pearson_r(valid_sim_rof, valid_obs_rof)
                runoff_nse = st.compute_nse(valid_sim_rof, valid_obs_rof)  
                runoff_pbias = st.compute_pbias(valid_sim_rof, valid_obs_rof)
                runoff_obj = 1 - runoff_nse

                sed_rmse = st.compute_rmse(valid_sim_sed, valid_obs_sed)
                sed_corr = st.pearson_r(valid_sim_sed, valid_obs_sed)
                sed_nse = st.compute_nse(valid_sim_sed, valid_obs_sed)
                sed_pbias = st.compute_pbias(valid_sim_sed, valid_obs_sed)
                sed_obj = 1 - sed_nse

                Obj_overall = runoff_obj+ sed_obj



            print(f"\n🟢 Runoff Results (Iteration {iteration})")
            print(f"Obj_func_rof= {runoff_obj:.4f}",f"NSE_rof= {runoff_nse:.4f}",f"PBIAS_rof= {runoff_pbias:.4f}",f"RMSE_rof= {runoff_rmse:.4f}",f"Corr.Coeff= {runoff_corr:.4f}")


            print(f"\n🟤 Sediment Results (Iteration {iteration})")
            print ( f"Obj_func= {sed_obj:.4f}",f"NSE= {sed_nse:.4f}",f"PBIAS= {sed_pbias:.4f}",f"RMSE= {sed_rmse:.4f}",f"Corr.Coeff= {sed_corr:.4f}")

            print(f"\n🟣 overall objective function = {Obj_overall:.4f}")


    return Obj_overall, runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias

