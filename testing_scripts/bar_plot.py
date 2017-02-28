'''
Created on Feb 28, 2017

@author: rsong_admin
'''
import matplotlib.pylab as plt
from matplotlib import style
from matplotlib.pyplot import cm 
import numpy as np
import pandas as pd

style.use('ggplot')

def plot_bar_TiO2():
        # TiO2
    market_name = ['Household & Furniture','Automotive','Medical','Other Industries','Packaging','Electronics',
                  'Construction & Building']
    amount = [1468.35487751, 540.792628124, 1122.57862278, 833.309532892, 1137.82004151, 863.93634447, 3705.56984166]
       
    width = 0.15
    last_num = 0
    color=iter(cm.Set1(np.linspace(0,1,7)))
    for name,num in zip(market_name,amount):
        c=next(color)
        if name == 'Construction & Building':
            plt.bar(0.1,num,width,bottom=last_num,color=c,label=name,yerr=3000,error_kw=dict(ecolor='rosybrown', lw=2, capsize=5, capthick=2))
        else:
            plt.bar(0.1,num,width,bottom=last_num,color=c,label=name)
         
        last_num += num
     
    plt.bar(0.7,39600,width,color='salmon',label = 'Static Results (aggregated, all uses)')
    plt.legend(loc='upper left')
    plt.xlim(0,1)
    plt.xticks((0.18,0.78), ('Dynamic Model','Static Model'))
    plt.tick_params(labelsize=14)
    plt.show()
    
def plot_bar_SiO2():
    df = pd.read_csv('../results/dynamic_results/SiO2_vintage_results_0226.csv',index_col=[0,1])
    market_name = ['Household & Furniture','Automotive','Medical','Other Industries','Packaging','Electronics',
                  'Construction & Building']
    amount=[df.loc[mat,'Manufacturing Release']['2010.0']+df.loc[mat,'In Use']['2010.0']+df.loc[mat,'End of Life']['2010.0'] for mat in market_name]
    
    width = 0.15
    last_num = 0
    color=iter(cm.Set1(np.linspace(0,1,7)))
    for name,num in zip(market_name,amount):
        c=next(color)
        if name == 'Construction & Building':
            plt.bar(0.1,num,width,bottom=last_num,color=c,label=name,yerr=1000,error_kw=dict(ecolor='rosybrown', lw=2, capsize=5, capthick=2))
        else:
            plt.bar(0.1,num,width,bottom=last_num,color=c,label=name)
    
        last_num += num
    
    plt.bar(0.7,9500,width,color='salmon',label = 'Static Results (aggregated, all uses)')
    plt.legend(loc='upper left')
    plt.xlim(0,1)
    plt.xticks((0.18,0.78), ('Dynamic Model','Static Model'))
    plt.tick_params(labelsize=14)
    plt.show()

def plot_bar_FeOx():
    # FeOx
    df = pd.read_csv('../results/dynamic_results/FeOx_vintage_results_0226.csv',index_col=[0,1])
    market_name = ['Household & Furniture','Automotive','Medical','Other Industries','Packaging','Electronics',
                  'Construction & Building']
    amount=[df.loc[mat,'Manufacturing Release']['2010.0']+df.loc[mat,'In Use']['2010.0']+df.loc[mat,'End of Life']['2010.0'] for mat in market_name]
    
    width = 0.15
    last_num = 0
    color=iter(cm.Set1(np.linspace(0,1,7)))
    for name,num in zip(market_name,amount):
        c=next(color)
        if name == 'Construction & Building':
            plt.bar(0.1,num,width,bottom=last_num,color=c,label=name,yerr=1000,error_kw=dict(ecolor='rosybrown', lw=2, capsize=5, capthick=2))
        else:
            plt.bar(0.1,num,width,bottom=last_num,color=c,label=name)
    
        last_num += num
    
    plt.bar(0.7,13860,width,color='salmon',label = 'Static Results (aggregated, all uses)')
    plt.legend(loc='upper left')
    plt.xlim(0,1)
    plt.xticks((0.18,0.78), ('Dynamic Model','Static Model'))
    plt.tick_params(labelsize=14)
    plt.show()
    
if __name__ == '__main__':

    plot_bar_FeOx()
 


