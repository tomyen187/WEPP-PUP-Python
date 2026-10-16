
import os
import datetime
import pandas as pd



class IterationLogger_all:
    def __init__(self, output_folder, parameters,restart_flag):
        """
        Initialize logger. Always overwrite old file if exists.
        """
        self.output_folder = output_folder
        self.log_file = os.path.join(output_folder, "All_iteration_result.csv")
        self.restart_flag=restart_flag
        # Prepare header
        header = ["Iteration", "Timestamp", "Best_obj_func.", "Current_obj_func.", "Current_runoff_rmse", "Current_runoff_corr", "Current_runoff_nse", "Current_runoff_pbias", "Current_sed_rmse","Current_sed_corr","Current_sed_nse","Current_sed_pbias"]

        header += [f"Best_{param['variable']}" for param in parameters]   # parameter names

        header += [f"Current_{param['variable']}" for param in parameters]   # parameter names

        if not restart_flag:		     # Overwrite if exists
   
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            with open(self.log_file, "w") as f:			#w - to write
                f.write(",".join(header) + "\n")

    def all_log_iteration(self, Iteration, Best_obj_func,Current_obj_func, Current_runoff_rmse, Current_runoff_corr, Current_runoff_nse, Current_runoff_pbias, Current_sed_rmse,Current_sed_corr,Current_sed_nse,Current_sed_pbias, param_values, current_param_values):
        """
        Append one iteration result into the log file.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            str(Iteration),
            timestamp,
            f"{Best_obj_func:.5f}",
            f"{Current_obj_func:.5f}",
            f"{Current_runoff_rmse:.4f}",
            f"{Current_runoff_corr:.4f}",
            f"{Current_runoff_nse:.4f}",
            f"{Current_runoff_pbias:.4f}",
            f"{Current_sed_rmse:.4f}",
            f"{Current_sed_corr:.4f}",
            f"{Current_sed_nse:.4f}",
            f"{Current_sed_pbias:.4f}",
        ]
        row += [str(val) for val in param_values]


        row += [str(val) for val in current_param_values]


        df_new = pd.DataFrame([row])
        df_new.to_csv(self.log_file, mode="a", header=False, index=False) 