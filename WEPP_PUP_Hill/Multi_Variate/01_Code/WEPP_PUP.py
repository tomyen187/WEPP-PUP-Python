import os
import csv
import shutil
import subprocess
import numpy as np
import time
import matplotlib.pyplot as plt

from parameter_update import update_parameter_file, read_parameter_file
from optimise import dds_sample, initial_sample
from wepp_run import run_wepp
from duplicate_input import prepare_working_inputs
from save_iter_result import IterationLogger
from save_all_iter import IterationLogger_all
from obj_plot import obj_func_plot
from IP import IP_uncertainty
from restart_manager import restart_iter
from Obj_mul_var_SY import objective_function_Mul




#######################################################  Def. main func. and Intial dec. of variables #####################################################

def WEPP_PUP_run(cli_file, param_file, Main_file, output_folder, working_folder,wepp_path, run_file_name, input_file, out_path, Obs_path, sed_obs_path, save_iter, max_iterations, ip_flag, MU_index,  optimization,restart_flag, calibration_start, calibration_end):
    
    os.system('clear')
    os.system('cls')
    start_time=time.time()

    print("""

  ***********************************************************************
  *								        *
  *                              WEPP-PUP                               * 
  *                  Water Erosion Prediction Project                   *
  *        Parameter estimation & Uncertainty analysis Program          *						
  *                          HILLSLOPE VERSION                          *
  *                             Developed by                            *
  *   Vijayalakshmi S.P : USDA-ARS-NSERL / Purdue University / IISc     *
  *      Haw Yen        : USDA-ARS-NSERL                                *
  *                                                                     *			
  *                      Last updated: 2026-Sep-30        	        *
  *								        *
  ***********************************************************************
""")		     
    
    
  
    if not os.path.exists(output_folder):			#creates
        os.makedirs(output_folder)

    for fname in os.listdir(output_folder):			#replaces
        if fname.startswith ("output"):
            os.remove(os.path.join(output_folder, fname))


    print(f"\n starts duplicating input folder ")
    
    prepare_working_inputs(Main_file, working_folder)				#duplicates the input folder to work currently

    parameters, lower_bounds, upper_bounds = read_parameter_file(param_file)	#read ini. cal_param file
									#++++  gets list of parameters cal. index ==1
    initial_values = [p['initial'] for p in parameters]
    lower_bounds = [p['lower'] for p in parameters]
    upper_bounds = [p['upper'] for p in parameters]
    param_evolution = [[] for _ in parameters]
    no_improve_counter = 0
    dim = len(parameters)
    all_samples = []
    param_new = []

 
    num_iterations = 1
    param_test = initial_values [:]							# stores all parameter value 
    runoff_compare_file = os.path.join(output_folder, "compare_runoff.txt")
    sed_compare_file = os.path.join(output_folder, "compare_sediment.txt")

    runoff_compare_folder = os.path.join(
        output_folder, "runoff compare for each iteration"
    )
    os.makedirs(runoff_compare_folder, exist_ok=True)

    sed_compare_folder = os.path.join(
        output_folder, "sed compare for each iteration"
    )
    os.makedirs(sed_compare_folder, exist_ok=True)


    logger = IterationLogger(output_folder, parameters, restart_flag)
    logger1 = IterationLogger_all(output_folder, parameters, restart_flag)


    print(f"\nSTART OF THE ITERATION ")


    # ==========================================================
    # 🔄 Restart Mechanism Check (move this here)
    # ==========================================================

    start_iter, param_best, best_score = restart_iter(save_iter, max_iterations, parameters, restart_flag)

    if start_iter is None:
        return
    #else:
       # start_iter, param_best, best_score = restart_iter(save_iter, max_iterations, parameters, restart_flag)

#################### Start of Initialization Computations ####################

### Start from random parameter set (or initial value if iteration = 1)		

    if not restart_flag:								

        for iteration in range(1,2):			
            print(f"\n🌀 Iteration {iteration}")
        
            param_test = initial_sample(iteration, param_test, lower_bounds, upper_bounds, param_new, parameters, working_folder,input_file,output_folder)

            for i, param in enumerate(parameters):
                if param['Cal_index'] == 1:
                    update_parameter_file(working_folder, param, param_test[i])
 

            new_cli_file= IP_uncertainty(iteration, run_file_name, cli_file, parameters, working_folder, ip_flag)    

            run_wepp(wepp_path, working_folder, run_file_name)												#ini_WEPP run	
               					   		 
            first_score,runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias = objective_function_Mul(output_folder, Obs_path,sed_obs_path, out_path, runoff_compare_file,sed_compare_file, iteration, MU_index, calibration_start, calibration_end)	# stores obj_func value
                 

            shutil.copy2( runoff_compare_file, os.path.join(runoff_compare_folder, f"runoff compare iteration {iteration}.txt") )

            shutil.copy2(
                sed_compare_file,
                os.path.join(
                    sed_compare_folder,
                    f"sed compare iteration {iteration}.txt"
                )
            )
                
            shutil.copy2(		#to save the output file gen. for each iteration
                out_path,
                os.path.join(
                    runoff_compare_folder,
                    f"out_path{iteration}.txt"
                )
            )
             

            param_best = param_test
            best_score = first_score

      
            logger.log_iteration(iteration,best_score, runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias,param_best) # li of parameter values
                                                      
               
            logger1.all_log_iteration(iteration, best_score, first_score, runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias, param_best, param_test)



#################### Start of DDS Computations ####################
  
    for iteration in range(max(start_iter, 2), max_iterations + 1):			#use when  restart mech. is needed else comment it

        
        print(f"\n🌀 Iteration {iteration}/{max_iterations}")

        param_test = dds_sample(optimization, param_best, lower_bounds, upper_bounds, num_iterations,max_iterations,parameters,input_file,output_folder)


#======== Update parameter files in working directory========

        for i, param in enumerate(parameters):
            if param['Cal_index'] == 1:
                update_parameter_file(working_folder, param, param_test[i])
                param_evolution[i].append(param_test[i])
     

        new_cli_file= IP_uncertainty(iteration, run_file_name, cli_file, parameters, working_folder, ip_flag)
        run_wepp(wepp_path, working_folder, run_file_name)  				#++++wepp run 2nd time 

          
        test_score, runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias =  objective_function_Mul(output_folder, Obs_path,sed_obs_path, out_path, runoff_compare_file,sed_compare_file, iteration,MU_index,calibration_start, calibration_end)        #obj_func after update

        shutil.copy2(
            runoff_compare_file,
            os.path.join(
                runoff_compare_folder,
                f"runoff compare iteration {iteration}.txt"
            )
        )

        shutil.copy2(
            sed_compare_file,
            os.path.join(
                sed_compare_folder,
                f"sed compare iteration {iteration}.txt"
            )
        )
                       
        shutil.copy2(		#to save the output file gen. for each iteration
            out_path,
            os.path.join(
                runoff_compare_folder,
                f"out_path{iteration}.txt"
            )
        )
               


        if test_score < best_score: 		#try to use < sign as the obj func dec. we need to minimise the obj func
            best_score = test_score		# if true updates obj. func score or value
            param_best = param_test.copy()	# appends and track best param. values
        

        
        logger.log_iteration(iteration, best_score,runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias
,param_best) # li of parameter values

        logger1.all_log_iteration(iteration, best_score, test_score, runoff_rmse, runoff_corr, runoff_nse, runoff_pbias, sed_rmse,sed_corr,sed_nse,sed_pbias, param_best, param_test)

    for i in range(dim):
        param_evolution[i].append(param_test[i])

#-----------------------------------stop criteria (if needed)---------------------------------------------

        
           # param_best=[val[0] if isinstance(val, list) else val for val in param_best]
           # for i in range (dim):
             #    param_best[i].copy(param_test[i])  # Append current param value to its record

            #no_improve_counter = 0		# counts how many iterations ran without improvement continusouly
        #else:
            #no_improve_counter += 1

        #if no_improve_counter >= 25:
            #print(f"Stopping early at iteration {iteration}: objective function has not improved for 25 consecutive steps.")
            #break

  


    # =====================================================
    # DDS probability plot
    # =====================================================


    iterations = list(range(1, max_iterations + 1))
    probabilities = [1 - (np.log(i) / np.log(max_iterations)) if i > 1 else 1 for i in range(1, max_iterations+1)]

    plt.figure(figsize=(8, 6))
    plt.plot(iterations, probabilities, label='DDS Probability', color='blue')
    plt.xlabel('Number of Iterations', fontname='Times New Roman', fontsize='12')
    plt.ylabel('Probability', fontname='Times New Roman', fontsize='12')
    plt.tight_layout()
    plt.title('DDS Iteration vs Probability', fontname='Times New Roman', fontsize='12')
    plt.legend()
    plot_path = os.path.join(output_folder, 'dds_probability_plot.png')
    plt.savefig(plot_path)
   # plt.close()

    
    # Plot parameter evolution
    for i, param_vals in enumerate(param_evolution):
        plt.figure(figsize=(8, 5))
        plt.plot(range(1, len(param_vals) + 1),param_vals)		
        plt.title(f"Current best of {parameters[i]['variable']}",fontname='Times New Roman', fontsize='12')
        plt.xlabel("Iteration", fontname='Times New Roman', fontsize='12')
        plt.ylabel("Value", fontname='Times New Roman', fontsize='12')
        plt.tight_layout()
        evol_path = os.path.join(output_folder, f"evolution_{parameters[i]['variable']}.png")
        plt.savefig(evol_path)
        #plt.show (block = False) 
        #plt.pause(1)			#pauses 1 sec.
       # plt.close()

    obj_func_plot(save_iter,output_folder)



    end_time = time.time()
    total_time = end_time - start_time
    print(f" \n total time taken to complete the run: {total_time: .2f} seconds")



if __name__ == '__main__':
    main()


