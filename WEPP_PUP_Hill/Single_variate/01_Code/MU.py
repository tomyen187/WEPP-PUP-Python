import numpy as np
import stats as st
import pandas as pd
from scipy.stats import norm, pearsonr
import os

 



def compute_uncertainty(compare_file, output, iteration):
    """
    Compute measurement uncertainty and performance metrics for runoff simulation.
    runoff_file : str, path to runoff_compare.csv file with columns Runoff_obs, Runoff_sim
    """
    # --- Step 1: Read file ---
    df = pd.read_csv(compare_file, sep='\s+')

    # --- Step 2: Filter valid values ---
    valid = df[(df["RoF_obs"] != -99) & (df["RoF_sim"] != -88)]
    valid_obs = valid["RoF_obs"].values
    valid_sim = valid["RoF_sim"].values

    if len(valid_obs) == 0:
        raise ValueError("No valid obs/sim pairs found in file.")

    # --- Step 3: Basic statistics ---
    mean_obs = np.mean(valid_obs)
    mean_sim = np.mean(valid_sim)
    std_obs = np.std(valid_obs, ddof=1)		# sample std_dev
    std_sim = np.std(valid_sim, ddof=1)
    var_obs = np.var(valid_obs, ddof=1)		#variance
    var_sim = np.var(valid_sim, ddof=1)


    # --- Step 4: Compute confidence factor (CF) ---
    CF_list = []

    a = valid_obs / 390.0
    std_dev = 42.0 * a

    for o, s, std in zip(valid_obs, valid_sim, std_dev):

        # A normal distribution cannot have scale=0.
        if std == 0:
            if s == o:
                cf = 0.0
            else:
                cf = 0.5

        elif abs(s - o) >= 3.9 * std:
            cf = 0.5 

        elif s >= o:
            cf = norm.cdf(s, loc=o, scale=std) - 0.5

        else:
            cf = 0.5 - norm.cdf(s, loc=o, scale=std)

        CF_list.append(cf)

    diff = valid_obs - valid_sim
    factor = np.asarray(CF_list, dtype=float) / 0.5
    adjusted_diff = factor * diff



    # --- Step 5: Performance metrics --- previous version
    rmse = np.sqrt(np.mean((adjusted_diff) ** 2))

    corr = st.pearson_r(valid_sim, valid_obs)

    nse = 1-np.sum((adjusted_diff) ** 2)/np.sum((valid_obs-mean_obs) ** 2)

    pbias= 100 * np.sum(adjusted_diff) / np.sum(valid_obs)
    obj_func = 1-nse


    # --- Step 6: Return results ---
    results = {
        "Iteration": iteration,
        "Mean_obs": mean_obs,
        "Mean_sim": mean_sim,
        "SD_obs": std_obs,
        "SD_sim": std_sim,
        "Var_obs": var_obs,
        "Var_sim": var_sim,
        "RMSE": rmse,
        "CC": corr,
        "NSE": nse,
        "Pbias": pbias,
        "Current_obj_func": obj_func
    }

   # print("Iteration stats:", results)
    MU_file = os.path.join(output, 'mu_results.xlsx')
    df_out = pd.DataFrame([results])
  


    if iteration == 1:
        # On the first iteration, we save fresh, overwriting any previous file
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


    return obj_func, rmse, corr, nse, pbias


























