import numpy as np
import pandas as pd
from scipy.stats import norm
import os
import stats as st  # our custom module with compute_rmse, compute_nse, pearson_r, etc. or use the default stats function there won't be any changes

def compute_uncertainty(compare_runoff,compare_sediment, output, iteration):


# --- Step 1: Read file ---

    df = pd.read_csv(compare_runoff, sep=r'\s+')

    df1 = pd.read_csv(compare_sediment, sep=r'\s+')

# --- Step 2: Filter valid data for runoff ---
    runoff_valid = df[(df["RoF_obs"] != -99) & (df["RoF_sim"] != -88)]
    sed_valid = df1[(df1["Sed_obs"] != -99) & (df1["Sed_sim"] != -88)]

    if runoff_valid.empty or sed_valid.empty:
        raise ValueError("No valid runoff or sediment observation-simulation pairs found.")

# --- Step 3: Extract values ---
    rof_obs = runoff_valid["RoF_obs"].values
    rof_sim = runoff_valid["RoF_sim"].values
    sed_obs = sed_valid["Sed_obs"].values
    sed_sim = sed_valid["Sed_sim"].values

# --- Step 4: Basic stats ---
    mean_rof_obs, mean_rof_sim = np.mean(rof_obs), np.mean(rof_sim)
    mean_sed_obs, mean_sed_sim = np.mean(sed_obs), np.mean(sed_sim)
    sd_rof_obs, sd_rof_sim = np.std(rof_obs, ddof=1), np.std(rof_sim, ddof=1)
    sd_sed_obs, sd_sed_sim = np.std(sed_obs, ddof=1), np.std(sed_sim, ddof=1)

# --- Step 5: Runoff Uncertainty (CF) ---
    a_rof = rof_obs / 390.0
    std_rof = 10.0 * a_rof
    #std_rof = np.where((np.isnan(std_rof)) | (std_rof == 0), 1e-6, std_rof)

    CF_runoff = []

    for o, s, sd in zip(rof_obs, rof_sim, std_rof):
    
        if s==o:
            cf_R = 0

        elif sd == 0:
            cf_R=0.5

        elif abs(s-o) >=3.9*sd:
            cf_R = 0.5

        elif s >= o:
            cf_R = norm.cdf(s, loc=o, scale=sd) - 0.5
        else:
            cf_R = 0.5 - norm.cdf(s, loc=o, scale=sd)

        CF_runoff.append(cf_R)

    diff_rof = (rof_obs-rof_sim)
    factor = np.asarray(CF_runoff, dtype=float)  / 0.5
    adjusted_diff_rof = factor * diff_rof
  


# --- Step 6: Sediment Yield Uncertainty (CF) ---
    a_sed = sed_obs / 390.0
    std_sed = 18.0 * a_sed   # ← changed multiplier to 18 for sediment
    std_sed = np.where((np.isnan(std_sed)) | (std_sed == 0), 1e-6, std_sed)

    CF_sediment = []
    for o, s, sd in zip(sed_obs, sed_sim, std_sed):

        if s==o:
            cf_S = 0

        elif sd == 0:
            cf_s=0.5

        elif abs(s-o) >=3.9*sd:
            cf_S = 0.5

        elif s >= o:
            cf_S = norm.cdf(s, loc=o, scale=sd) - 0.5
        else:
            cf_S = 0.5 - norm.cdf(s, loc=o, scale=sd)
        CF_sediment.append(cf_S)


    diff_sed = (sed_obs-sed_sim)
    factor = np.asarray(CF_sediment, dtype=float) / 0.5
    adjusted_diff_sed = factor * diff_sed
  



# --- Step 7: Performance metrics ---
# Runoff
    rmse_rof = np.sqrt(np.mean((adjusted_diff_rof) ** 2))
    corr_rof = st.pearson_r(rof_sim, rof_obs)
    nse_rof = 1-np.sum((adjusted_diff_rof) ** 2)/np.sum((rof_obs-mean_rof_obs) ** 2)
    pbias_rof = 100 * np.sum(adjusted_diff_rof) / np.sum(rof_obs)
    obj_func_rof = 1 - nse_rof

# Sediment
    rmse_sed = np.sqrt(np.mean((adjusted_diff_sed) ** 2))
    corr_sed = st.pearson_r(sed_sim, sed_obs)
    nse_sed = 1-np.sum((adjusted_diff_sed) ** 2)/np.sum((sed_obs-mean_sed_obs) ** 2)
    pbias_sed = 100 * np.sum(adjusted_diff_sed) / np.sum(sed_obs)
    obj_func_sed = 1 - nse_sed

    Obj_func = obj_func_rof + obj_func_sed


    

    print(f"\n🟢 Runoff Results (Iteration {iteration})")
    print(f"Obj_func_rof= {obj_func_rof:.4f}",f"NSE_rof= {nse_rof:.4f}",f"PBIAS_rof= {pbias_rof:.4f}",f"RMSE_rof= {rmse_rof:.4f}",f"Corr.Coeff=    {corr_rof:.4f}")


    print(f"\n🟤 Sediment Results (Iteration {iteration})")
    print ( f"Obj_func= {obj_func_sed:.4f}",f"NSE= {nse_sed:.4f}",f"PBIAS= {pbias_sed:.4f}",f"RMSE= {rmse_sed:.4f}",f"Corr.Coeff= {corr_sed:.4f}")

    print(f"\n🟣 overall objective function = {Obj_func:.4f}")


# --- Step 8: Combine results ---
    results = {
        "Iteration": iteration,

    # Runoff stats
        "Mean_RoF_obs": mean_rof_obs,
        "Mean_RoF_sim": mean_rof_sim,
        "SD_RoF_obs": sd_rof_obs,
        "SD_RoF_sim": sd_rof_sim,
        "RMSE_RoF": rmse_rof,
        "CC_RoF": corr_rof,
        "NSE_RoF": nse_rof,
        "Pbias_RoF": pbias_rof,
        "ObjFunc_RoF": obj_func_rof,

    # Sediment stats
        "Mean_Sed_obs": mean_sed_obs,
        "Mean_Sed_sim": mean_sed_sim,
        "SD_Sed_obs": sd_sed_obs,
        "SD_Sed_sim": sd_sed_sim,
        "RMSE_Sed": rmse_sed,
        "CC_Sed": corr_sed,
        "NSE_Sed": nse_sed,
        "Pbias_Sed": pbias_sed,
        "ObjFunc_Sed": obj_func_sed,
        "Obj_func": Obj_func
    }





# --- Step 9: Save to CSV (append if exists) ---
    MU_file = os.path.join(output, "mu_results.xlsx")
    df_out = pd.DataFrame([results])




    if iteration == 1:
        # On the first iteration, we save fresh, overwriting any previous file
        if os.path.exists(MU_file):
            os.remove(MU_file)
	   # MU_file = os.path.join(output, "mu_results.xlsx")
        df_out.to_excel(MU_file, index=False)
    else:
        # For subsequent iterations, we read the existing file and append the new row
        if os.path.exists(MU_file):
            existing_df = pd.read_excel(MU_file)
            updated_df = pd.concat([existing_df, df_out], ignore_index=True)
            updated_df.to_excel(MU_file, index=False)
        else:
            # Fallback in case iteration 1 was skipped or file was deleted
            df_out.to_excel(MU_file, index=False)



# --- Step 10: Return both results (runoff + sediment) ---
    return (Obj_func, rmse_rof, corr_rof, nse_rof, pbias_rof, rmse_sed, corr_sed, nse_sed, pbias_sed)

