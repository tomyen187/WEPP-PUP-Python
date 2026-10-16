import numpy as np
import math
from statistics import mean
from scipy.stats import pearsonr

def compute_corr(sim,obs):
    
    corr = np.corrcoef(sim, obs)
    print(f"Correlation coefficient: {corr}")


def compute_rmse(sim, obs):
    rmse= math.sqrt(sum((s - o) ** 2 for s, o in zip(sim, obs)) / len(obs))
    return rmse

        
def compute_r2(sim, obs):
    mean_obs = mean(obs)
    ss_tot = sum((o - mean_obs) ** 2 for o in obs)
    ss_res = sum((o - s) ** 2 for o, s in zip(obs, sim))
    a = 1 - (ss_res / ss_tot, ss_tot != 0)
    return a

def compute_pbias(sim, obs):
    
    if not obs or sum(obs)== 0:
        print("⚠️ Observed data is empty or all zeros. Cannot compute PBIAS.")
        return float('nan') 
    
    if not sim:
        print("⚠️ Simulated data is empty. Cannot compute PBIAS.")
        return float('nan')
        
    p_bias= 100.0 *((sum(o - s for o, s in zip(obs, sim))) / (sum(obs)))
    return p_bias

def compute_nse (sim, obs):
    mean_obs=mean(obs)
    nse  = 1 - sum((o - s) ** 2 for o, s in zip(obs, sim)) / (sum((o - mean_obs) ** 2 for o in obs))
    return nse


def pearson_r (sim, obs):
    r, _ = pearsonr(obs, sim)
  
    return r
    #return r, _ to get both the values r and error_bias ...

