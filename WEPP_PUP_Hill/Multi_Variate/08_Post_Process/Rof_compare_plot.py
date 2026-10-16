import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

from scipy import stats

def calc_statistics(obs, sim):
    obs = np.array(obs)
    sim = np.array(sim)

    mask = ~np.isnan(obs) & ~np.isnan(sim)
    obs = obs[mask]
    sim = sim[mask]

    if len(obs) == 0:
        return np.nan, np.nan, np.nan

    rmse = np.sqrt(np.mean((obs - sim) ** 2))
    nse = 1 - (np.sum((obs - sim) ** 2) / np.sum((obs - np.mean(obs)) ** 2))
    pbias = 100 * np.sum(sim - obs) / np.sum(obs)

    return rmse, nse, pbias

def plot_runoff(compare_runoff,out_dir):

    df=pd.read_csv(compare_runoff, sep = "\t")

# Observed runoff date
    df['date_obs'] = pd.to_datetime(df[['Yr_obs', 'Mon_obs', 'Day_obs']].rename(columns={'Yr_obs': 'year', 'Mon_obs': 'month', 'Day_obs': 'day'}))

# Simulated runoff date (if present)
    if {'Yr_sim', 'Mon_sim', 'Day_sim'}.issubset(df.columns):
        df['date_sim'] = pd.to_datetime(df[['Yr_sim', 'Mon_sim', 'Day_sim']].rename(columns={'Yr_sim': 'year', 'Mon_sim': 'month', 'Day_sim': 'day'}))

    #df['date_obs']=pd.to_datetime(df[['Yr_obs', 'Mon_obs', 'Day_obs']])
    #df['date_sim']=pd.to_datetime(df[['Yr_sim', 'Mon_sim', 'Day_sim']])		
    
    df['obs_RF']=pd.to_numeric(df['RoF_obs'], errors= 'coerce')
    df['sim_RF']=pd.to_numeric(df['RoF_sim'], errors= 'coerce')

    # Replace non-data values with NaN

    df.loc[df['RoF_obs'].isin([-88, -99]), 'RoF_obs'] = None		# obs = df["RoFobs"].replace([-88, -99], np.nan)
    df.loc[(df['RoF_sim'].isin([-88, -99,]) | (df['RoF_obs'] < 1)), 'RoF_sim'] = None

#stats

    obs = df['RoF_obs']
    sim = df['RoF_sim']
    rmse, nse, pbias = calc_statistics(obs, sim)

#plot scatter

    #fig, ax1 = plt.subplots(figsize=(10,6))
    
    #primary y - axis (obs)

    plt.figure(figsize=(8,8))
    plt.xlabel("Observed Runoff (mm)", fontsize = 12,fontname='Times New Roman')
    plt.ylabel("Simulated Runoff (mm)", fontsize= 12, fontname = 'Times New Roman')
    plt.scatter(df['RoF_obs'],df['RoF_sim'],color='blue',alpha = 0.2)
    
    np.random.seed(42) # for reproducibility
    x_data = np.random.rand(80) * 100
    y_data = x_data * 0.8 + np.random.randn(80) * 2 + 1
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)

    min_val = min(x_data.min(), y_data.min())
    max_val = max(x_data.max(), y_data.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', label='1:1 Line')

    plt.title("Observed Vs Simulated Runoff",fontsize= 12, fontname = 'Times New Roman')
    plt.legend()
    plt.tight_layout()
    save_plot=os.path.join(out_dir, "runoff_compare.jpg")
    plt.savefig(save_plot,dpi=300)
    plt.close()
       
    print(f"✅ Plot saved at: {save_plot}")


#plot line

    fig, ax1 = plt.subplots(figsize=(10,6))
    
    #primary y - axis (obs)

    ax1.set_xlabel("Date")
    ax1.set_ylabel("Observed Runoff (mm)", fontsize = 12,fontname='Times New Roman',color='blue')
    ax1.plot(df['date_obs'],df['RoF_obs'],color='blue',linewidth = 0.75)
    ax1.tick_params(axis='y', labelcolor='blue')			#if needed uncomment it


    #sec. y - axis (sim)
    
    ax2=ax1.twinx()
    ax2.set_ylabel("Simulated Runoff (mm)", fontsize= 12, fontname = 'Times New Roman',color='red')
    ax2.plot(df['date_sim'], df['RoF_sim'], color = 'red', linewidth = 0.75)		#linestyle="--" --if needed
    ax2.tick_params(axis='y', labelcolor='red')			#if needed uncomment it


    plt.legend()
    plt.title("Observed Vs Simulated Runoff ")
    
    fig.tight_layout()
    save_plot=os.path.join(out_dir, "runoff_compare_line.jpg")
    plt.savefig(save_plot,dpi=300)
    plt.close()
       
    print(f"✅ Plot saved at: {save_plot}")

if __name__ == "__main__":		#it is like .exe file if you want to call this fnc. in another file delete this section


    out_dir = r"...\Multi_variate\output"
    compare_runoff = r"...\Multi_variate\runoff_compare.txt" 		#create your own comparison file for validation period

    plot_runoff(compare_runoff, out_dir)

































