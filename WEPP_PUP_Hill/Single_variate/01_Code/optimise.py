import random
import math
import matplotlib.pyplot as plt
from parameter_update import update_parameter_file
from PRS import PRS_sample


def initial_sample(iteration,current_best, lower_bounds, upper_bounds, param_new,parameters,working_folder,input_file,output_folder):
    """
    Generate a DDS sample by randomly selecting new values 
    uniformly within the given lower and upper bounds.
    """
   
    				# this was there initially: current_best = ini_val.copy()
    dim = len(current_best)


    if iteration == 1:
        param_new = current_best.copy()		#  Use initial values directly
        

    # ---------------------------------------------------------
    # Safety check
    # ---------------------------------------------------------

    if len(param_new) != dim:

        raise ValueError(
            f"initial_sample produced {len(param_new)} values "
            f"for {dim} parameters."
        )

    if any(
        isinstance(value, (list, tuple))
        for value in param_new
    ):

        raise TypeError(
            "initial_sample must return numeric parameter values, "
            f"but returned: {param_new}"
        )
                
    return param_new


#==============================================================================



def _reflect_bounds(new_val, lower_bound, upper_bound):
    """
    DDS reflective boundary handling.
    """

    if lower_bound >= upper_bound:
        return lower_bound

    if new_val < lower_bound:

        new_val = (
            lower_bound
            + (lower_bound - new_val)
        )

        if new_val > upper_bound:
            new_val = lower_bound

    elif new_val > upper_bound:

        new_val = (
            upper_bound
            - (new_val - upper_bound)
        )

        if new_val < lower_bound:
            new_val = upper_bound

    return new_val

#========================================================================


def dds_sample(optimization, current_best, lower_bounds, upper_bounds, iteration, max_iterations, parameters,input_file,output_folder):
    """
    Generate a new candidate using DDS logic.
    
    Parameters:
    - current_best: List of current best parameter values.
    - lower_bounds, upper_bounds: Lists of bounds for each parameter.
    - iteration: Current iteration count (starting at 1).
    - max_iterations: Total number of iterations to run.

    Returns:
     - new_params: List of parameter values sampled by DDS.
    """
    
    if optimization == 0:		#default

        current_best = current_best.copy()				# this was there initially: current_best = ini_val.copy()
        dim = len(current_best)
       # all_samples = [current_best.copy()]
       # best_value = [[] for _ in range(dim)]

        if dim == 0:

            raise ValueError(
                "No active calibration parameters "
                "were supplied to DDS."
            )

        if (
            len(lower_bounds) != dim
            or len(upper_bounds) != dim
        ):

            raise ValueError(
                "current_best, lower_bounds and upper_bounds "
                "must have equal lengths."
            )
    
  

    # Probability of perturbation decreases as search progresses.......... Initialize best_value correctly if it's empty
       

        #for iteration in range(1, max_iterations + 1):
        perturbation_prob = (1 - (math.log(iteration) /math.log( max_iterations)))
        perturbation_prob = max(0.0, min(1.0, perturbation_prob))
        new_params = current_best.copy()
        perturbed_indices = set()

        # -------------------------------------------------
        # STEP 1:
        # Select dimensions using U(0,1)
        # -------------------------------------------------

        for i in range(dim):
            if random.random() < perturbation_prob:			# earlier: if random.gauss(0,1) < perturbation_prob or len(perturbed_indices) == 0:

                perturbed_indices.add(i)

        # DDS must perturb at least one parameter.
        if len(perturbed_indices) == 0:

            perturbed_indices.add(
                random.randrange(dim)
            )


        # -------------------------------------------------
        # STEP 2:
        # Perturb selected parameters using N(0,1)
        # -------------------------------------------------

        for i in perturbed_indices:
            range_span = upper_bounds[i] - lower_bounds[i]   # mean = 0; std_dev = 1
            perturbation = 0.2 	
            new_val = current_best[i] + perturbation*range_span*random.gauss(0, 1)		#earlier  new_val = new_params[i] + perturbation*range_span*random.gauss(0, 1)	
           # print ("new_val", new_val)
	                
	    
            new_val = _reflect_bounds(new_val,lower_bounds[i],upper_bounds[i])

            #new_val = max(lower_bounds[i], min(upper_bounds[i], new_val))		  # Clamp to bounds
	        
            new_params[i] = new_val

  

    else:
        new_params = PRS_sample(optimization, current_best, lower_bounds, upper_bounds, iteration, max_iterations,parameters,input_file,output_folder)


    return new_params























