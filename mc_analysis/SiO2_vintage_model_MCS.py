'''
Created on Mar 15, 2016
A caller to calculate the SiO2 vintage release 

Year 1970 - Year 2020
@author: rsong_admin
'''
import sys
sys.path.append('../packages')

'''Change 26/12/2016 by Yuwei'''
import os
os.chdir("../packages")
'''Done'''
import vintage_model
import numpy as np
import csv
import matplotlib.pylab as plt
from monte_carlo_lifetime import *
from matplotlib import style
style.use('ggplot')

'''
Calculate the average case
'''
'''Change 26/12/2016 by Yuwei'''
def csv_to_dict(csv_file):
    with open(csv_file,'rU') as myfile:
        this_reader = csv.reader(myfile)
        # skip the header row
        next(this_reader, None)
        ''' row[0] is the sector name; row[1] percentage; row[2] average_lifetime; row[3] is the in use release rate '''
        market_dict = {rows[0]:[rows[1],\
                                float(np.random.triangular(rows[6],rows[2],rows[7])),\
                                float(np.random.triangular(0.1,0.5,0.9)),\
                                rows[4],rows[5],rows[6],rows[7]] for rows in this_reader}
    #print(market_dict)
    return market_dict
'''done'''

def calculate_defult_SiO2():
    '''
    Do a single vintage calculation
    default market share  = 0.1
    '''
    # read data now
    SiO2_data = np.loadtxt('../data/SiO2_production_real.csv',delimiter=',')
    SiO2_to_paints = 0.1 # what portion of SiO2 are used in coating, paints and pigment market
    SiO2_data[:,1] = SiO2_data[:,1] * SiO2_to_paints
    market_data_dict = csv_to_dict('../data/coating_market_fake.csv')
    
    SiO2_market = vintage_model.vintage_market(SiO2_data,market_data_dict, weibull=True)
    test = SiO2_market.calculate_market_vintage()
    
    '''Change 26/12/2016 by Yuwei'''
    table_of_test = np.zeros((35,21))
    
    row_num_in_table = 0
    for index in range(len(test)): #find each category e.g. Household & Furniture
        index_in_test = test[test.keys()[index]] #create a table of test
        for num in range(len(index_in_test)): #num is each phase
            list_in_index = index_in_test[index_in_test.keys()[num]]
            #print(list_in_index) # save number in each phase e.g. manufacturing, in use
            #print(row_num_in_table)
            for val in range(len(list_in_index)): #val is year
                #print(val)
                table_of_test[row_num_in_table,val] = list_in_index[val]
            row_num_in_table += 1
    #print(table_of_test)
    #print np.sum(test['Household & Furniture']['In Use'] + test['Household & Furniture']['End of Life'])
    #raw_input()
    
    table_of_sum = np.zeros([1,21])   
    
    '''sum up the total release for each year '''
    for i in range(21):
        #print(i)
        '''only sum up manufacturing release, in use and end of life 
        (row: 5n,5n+1,5n+2) '''
        sum = 0
        for row in range(7):
            sum += table_of_test[5*row,i]+table_of_test[5*row+1,i]+table_of_test[5*row+2,i]
        table_of_sum[0,i] = sum
         
    #print(table_of_sum)   
    return table_of_sum
    
#     df = FeO2_market.to_dataframe(test)
#     FeO2_market.plot_market_vintage()
#     df.to_csv('../results/dynamic_results/FeOx_vintage_results_1215.csv')
#     df.to_csv('../results/static_results/FeOx_vintage_results_static_1215.csv')
    '''  done'''

'''Change 12/31/2016 by Yuwei'''
def monte_carlo_cal():

    # create local list to store MCS values
    for n in range(1):
        for m in range(21):
            locals()['L_'+str(n)+'_'+str(m)] = []
    # calculate MCS and store the values
    for i in range(10000):
        print(i)
        #run results 
        result = calculate_defult_SiO2()
        for n in range(1):
            for m in range(21):
                locals()['L_'+str(n)+'_'+str(m)].append(result[n,m])
    
    
    # create table to store mean, median, sd, 2.5%, 97.5%, and CV
    table_mean = np.zeros([1,21])
    table_percent25 = np.zeros([1,21])
    table_percent975 = np.zeros([1,21])
    
    # calculate mean, median, sd, 2.5%, 97.5%, CV
    for n in range(1):
        for m in range(21):    
            lst = locals()['L_'+str(n)+'_'+str(m)]
            mean = np.mean(lst)
            percent25 = np.percentile(lst,2.5) 
            percent975 = np.percentile(lst,97.5)
        
            table_mean[n,m] = mean
            table_percent25[n,m] = percent25
            table_percent975[n,m] = percent975
            
    #print os.getcwd()  
    np.savetxt('../results/MCS_sum_results/SiO2_MCS_sum_mean.csv',table_mean,delimiter = ',')
    np.savetxt('../results/MCS_sum_results/SiO2_MCS_sum_percent25.csv',table_percent25,delimiter = ',') 
    np.savetxt('../results/MCS_sum_results/SiO2_MCS_sum_percent975.csv',table_percent975,delimiter = ',') 
'''done'''  
    
def do_shake_lifetime():
    data = './data/SiO2_production_real.csv'
    market = './data/coating_market_fake.csv'
    SiO2_to_coating = 0.1
    this_shaker = lifetime_shaker(data,market,SiO2_to_coating)
    MT_results = this_shaker.monte_carlo_analysis(round=500)
    average_tot = calculate_defult_SiO2()
    this_shaker.plot_error_bar(MT_results,average_tot)

def do_release_market():
    SiO2_data = np.loadtxt('./data/SiO2_production_real.csv',delimiter=',')
    market_data_dict = csv_to_dict('./data/coating_market_fake.csv')
    SiO2_to_coating = 0.1
    SiO2_data[:,1] = SiO2_data[:,1] * SiO2_to_coating
    SiO2_market = vintage_model.vintage_market(SiO2_data,market_data_dict)
    test = SiO2_market.calculate_market_vintage()
    print SiO2_market.tot_releases_year()
    SiO2_market.plot_market_vintage('')
    
    
if __name__ == '__main__':
    '''Change 12/31/2016 by Yuwei'''
    monte_carlo_cal()
    '''DONE'''