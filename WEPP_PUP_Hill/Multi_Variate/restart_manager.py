
import os
import pandas as pd
import numpy as np

def restart_iter(save_iter_file, max_iterations,parameters, restart_flag):
    """
    Manages restart for DDS calibration loop.
    
    Parameters
    ----------
        restart_flag : bool
        True → restart mechanism enabled, 
        False → start from iteration 1 fresh.
    """

    start_iter = 1
    param_best= None
    best_score = None
    

    if restart_flag and os.path.exists(save_iter_file):
        try:
            df = pd.read_csv(save_iter_file)
            if not df.empty:
                last_row = df.iloc[-1]

                non_param_cols = {"Iteration", "Timestamp", "Score", "runoff_rmse", "runoff_corr", "runoff_nse", "runoff_pbias", "sed_rmse","sed_corr","sed_nse","sed_pbias"}

                param_cols = [col for col in df.columns if col not in non_param_cols]
                last_params = {p["variable"]: float(last_row[p["variable"]]) for p in parameters if p["Cal_index"] == 1}
                               

                last_iter = int(df["Iteration"].iloc[-1])	#or  last_iter= df.loc[df["Iteration"] == start_iter].iloc[0]
                Score = float(df["Obj_Func."].iloc[-1])
                start_iter = last_iter + 1
                best_score = Score
                param_best = [last_params[p["variable"]] for p in parameters if p["Cal_index"] == 1]
                #print("lastparam:",last_params)

                print(f"🔄 Restarting from Iteration {start_iter} using saved parameters.")
            else:
                print("ℹ️ iteration result exists but is empty. Starting fresh.")
        except Exception as e:
            print(f"⚠️ Could not read iteration result Starting fresh. Error: {e}")
    #else:
       # print("ℹ️ Restart not requested or iteration result not found. Starting fresh.")

    if start_iter > max_iterations:
        print("✅ All iterations already completed. Nothing to restart.")
        return None, None,None
  
    return start_iter, param_best, best_score
