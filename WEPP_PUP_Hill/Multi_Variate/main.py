

from WEPP_PUP import WEPP_PUP_run

param_file = r'V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\03_Parameter\WEPP_PUP_cal_param.txt'  		# contains the parameters
Main_file =  r'V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\02_Input_files'  				#main input
output_folder = r'V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\06_Output'
working_folder =r'V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\05_Working_Inputs'
wepp_path = r"V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\04_WEPP\wepp_2012.exe"
  
run_file_name = r"p0.run"
input_file = r'V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\05_Working_inputs\p0.sol'
out_path= r"V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\06_Output\evbe_1.txt" 	
Obs_path = r"V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\05_Working_inputs\cont_obs_runoff_Mul_var.txt"	
sed_obs_path = r'V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\02_Input_files\cont_obs_sed_Mul_var.txt'
save_iter = r"V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\06_Output\iteration_result.csv" 
cli_file= r'V:\acerlaptop\WEPP_PUP_HILL\Multi_variate\05_Working_inputs\p0.cli'



calibration_start = "1995-01-01"
calibration_end = "2009-12-31"

WEPP_PUP_run(cli_file, 
    param_file,
    Main_file,
    output_folder,
    working_folder, 
    wepp_path,  
    run_file_name, 
    input_file, 
    out_path, 
    Obs_path, 
    sed_obs_path,
    save_iter,
    max_iterations = 1000,
    ip_flag=0,
    MU_index=0,
    optimization=0,
    restart_flag=0,
    calibration_start=calibration_start,
    calibration_end=calibration_end)



# Input uncertainty- yes, ip_flag = 1, Also enable sigma and nu =1 in WEPP_PUP_cal_param.txt; if it is No: ip_flag = 0, disable sigma and nu = 0 in WEPP_PUP_cal_param.txt

# Measurement uncertainty- yes, MU_index = 1; No MU_index = 0

#if the WEPP-PUP code crashes halfway give restart_flag=1; else = 0

#optimization=0: runs DDS optimisation algorithm by default; if its 1: PRS algorithm


