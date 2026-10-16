import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from datetime import datetime
import numpy as np


def obj_func_plot(save_iter, output):

    df=pd.read_csv(save_iter)
    Iteration = df['Iteration']
    Obj_fun= df['Obj_Func.']
    font_prop = fm.FontProperties(family='Times New Roman', size=12)

    plt.figure(figsize=(10,6))
    plt.plot(Iteration,Obj_fun,label='Objective Function', color='purple')
    plt.xlabel('No. of Iteration', fontsize=12, fontname='Times New Roman')
    plt.ylabel('Objective Function Value', fontsize=12, fontname='Times New Roman')
    plt.title('Objective Function',fontsize=12, fontname='Times New Roman')
    plt.legend(prop=font_prop)
    plt.tight_layout() 
    save_plot=os.path.join(output, "obj_func_plt.jpg")
    plt.savefig(save_plot)
   # plt.show() 
    #plt.close()


