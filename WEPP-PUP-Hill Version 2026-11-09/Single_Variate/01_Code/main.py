from WEPP_PUP import WEPP_PUP_run

param_file = r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\03_Parameter\WEPP_PUP_cal_param.txt'  		
main_file = r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\02_Input_Files'  				
output_folder = r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\06_Output'
working_folder =r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\05_Working_Inputs'
wepp_path = r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\04_WEPP\wepp_2012.exe'
input_file = r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\05_Working_Inputs\p0.sol'
out_path= r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\06_Output\evbe_1.txt'
obs_path = r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\05_Working_Inputs\continuous_observed_runoff.txt'			#earlier the run was made using this file
save_iter = r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\06_Output\iteration_result.csv'
cli_file= r'V:\acerlaptop\WEPP_PUP_HILL\Single_variate\05_Working_Inputs\p0.cli'

run_file_name = r"p0.run"

calibration_start = "1963-01-01"
calibration_end = "1992-12-31"


WEPP_PUP_run(cli_file,
    param_file, 
    main_file,
    output_folder, 
    working_folder,
    wepp_path, 
    run_file_name,
    input_file,
    out_path, 
    obs_path,
    save_iter,
    max_iterations = 1000,
    ip_flag=0, 
    MU_index=0,
    optimization=0, 
    restart_flag=0,
    calibration_start=calibration_start,
    calibration_end=calibration_end)



# Input uncertainty- yes, ip_flag = 1; No ip_flag = 0, Also enable sigma and nu =1 in WEPP_PUP_cal_param.txt

# Measurement uncertainty- yes, MU_index = 1; No MU_index = 0

#if the WEPP-PUP code crashes halfway give restart_flag=1; else = 0

#optimization=0: runs DDS optimisation algorithm by default; if its 1: PRS algorithm
