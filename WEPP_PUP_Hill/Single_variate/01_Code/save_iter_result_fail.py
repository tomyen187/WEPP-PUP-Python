
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
        header = ["Iteration", "Timestamp", "Obj_Func.", "RMSE", "PBIAS", "CORR", "NSE"]
        header += [param["variable"] for param in parameters]   # parameter names
        if not restart_flag:		     # Overwrite if exists
   
            if os.path.exists(self.log_file):
                os.remove(self.log_file)

          
    def log_iteration(self, Iteration, Obj_Func,
                      rmse, pbias, corr, nse, param_values):
        """
        Append one iteration result into the log file.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = [
            str(Iteration),
            timestamp,
            f"{Obj_Func:.5f}",
            f"{rmse:.4f}",
            f"{pbias:.4f}",
            f"{corr:.4f}",
            f"{nse:.4f}"
        ]
        row += [str(val) for val in param_values]

        df_new = pd.DataFrame([row])
        df_new.to_csv(self.log_file, mode="a", header=False, index=False) 

          


#-------------hill version






















