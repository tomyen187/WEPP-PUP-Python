
import os
import datetime
import pandas as pd


class IterationLogger:
    def __init__(self, output_folder, parameters,restart_flag):
        """
        Initialize logger. Always overwrite old file if exists.
        """
        self.output_folder = output_folder
        self.log_file = os.path.join(output_folder, "iteration_result.csv")
        self.restart_flag=restart_flag
        # Prepare header
        header = ["Iteration", "Timestamp", "Obj_Func.", "runoff_rmse", "runoff_corr", "runoff_nse", "runoff_pbias", "sed_rmse","sed_corr","sed_nse","sed_pbias"]
        header += [param["variable"] for param in parameters]   # parameter names
        if not restart_flag:		     # Overwrite if exists
   
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            with open(self.log_file, "w") as f:			#w - to write
                f.write(",".join(header) + "\n")

    def log_iteration(self, Iteration, Obj_Func, runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias, param_values):
        """
        Append one iteration result into the log file.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            str(Iteration),
            timestamp,
            f"{Obj_Func:.5f}",
            f"{runoff_rmse:.4f}",
            f"{runoff_corr:.4f}",
            f"{runoff_nse:.4f}",
            f"{runoff_pbias:.4f}",
            f"{sed_rmse:.4f}",
            f"{sed_corr:.4f}",
            f"{sed_nse:.4f}",
            f"{sed_pbias:.4f}",
        ]
        row += [str(val) for val in param_values]

        df_new = pd.DataFrame([row])
        df_new.to_csv(self.log_file, mode="a", header=False, index=False) 














