import random
import matplotlib.pyplot as plt
#import objective_function
#from objective_function import objective_function
from parameter_update import update_parameter_file



def PRS_sample(optimization, ini_val, lower_bounds, upper_bounds, iteration, max_iterations, parameters,input_file,output_folder):
    """
    Generate a new candidate using DDS logic.
    
    Parameters:
    - ini_val: List of current best parameter values.
    - lower_bounds, upper_bounds: Lists of bounds for each parameter.
    - iteration: Current iteration count (starting at 1).
    - max_iterations: Total number of iterations to run.

    Returns:
     - new_params: List of parameter values sampled by PRS.
    """
    #print("PRS lgorithm running")

    if optimization == 1: 
       
        current_best = ini_val				
        dim = len(current_best)
        new_params = current_best.copy()

        for i in range(dim):

            range_span = upper_bounds[i] - lower_bounds[i]   
            new_val = lower_bounds[i] + range_span*random.uniform(0, 1)	
            new_params[i] = new_val
  



        

    return new_params























