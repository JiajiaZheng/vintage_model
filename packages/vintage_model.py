'''
Created on Mar 4, 2016

@author: rsong_admin
'''
import numpy as np
import csv
import copy
import pandas as pd
import copy
from scipy.special import gammaln
import matplotlib.pylab as plt
from matplotlib import style
from matplotlib.pyplot import cm 

style.use('ggplot')

class vintage_market:
    '''
    A wrapper class to deal with the situation with multiply market
    '''
    def __init__(self,production_data, market_data_dict, weibull = True):
        self.year_and_prod = production_data
        self.tot_prod = production_data[:,1]
        self.years = production_data[:,0]
        ''' split market data '''
        self._market_splitter(market_data_dict)
        
        self.if_weibull = weibull
      
    def _market_splitter(self,market_data_dict):
        '''
        market data file reader
        
        Input -- market data file, the first column is the name of the sector
                 the second column is the percentage of each sector, the third column is the average lifetime of this sector
        Return -- A dictionary contain sector name and break down
        '''
#
        ''' market_data_file is now a dictionary now'''
        self.market_dict = market_data_dict 
        self.prod_dict = {}
        for each_mak, each_val in self.market_dict.iteritems():
            ''' create a dictionary that contain the production data flows into each market
                for example : Buildings: 89000*45% tons
                each_val[0] is the percentage
            '''
            this_mark_year_prod = self.year_and_prod.copy()
            this_mark_year_prod[:,1] = this_mark_year_prod[:,1]*float(each_val[0])

            self.prod_dict[each_mak] = this_mark_year_prod  
            
    def calculate_market_vintage(self):
        '''
        wrapper function to call the vintage class by market share
        '''
        assert self.prod_dict is not None
        self.market_vintage_results = {}
 
        for each_mak, each_val in self.prod_dict.iteritems():
            this_lifetime = self.market_dict[each_mak][1]
            this_in_use = self.market_dict[each_mak][2]
            this_repaint_freq = self.market_dict[each_mak][3]
             
            this_prod_data = each_val
             
            this_market = vintage(this_prod_data,this_lifetime,this_in_use,repaint_freq=this_repaint_freq, weibull=self.if_weibull)
            this_vintage = this_market.calculate_vintage()
            self.market_vintage_results[each_mak] = this_vintage 
 
        return self.market_vintage_results
    
    def calculate_for_one_vintage(self, year):
        self.vintage_results_for_one_year = {}
        this_year = year - 2000

        for each_mak, each_val in self.prod_dict.iteritems():
            this_lifetime = self.market_dict[each_mak][1]
            this_in_use = self.market_dict[each_mak][2]
            this_repaint_freq = self.market_dict[each_mak][3]
            
            this_prod_data = each_val
            this_year_prod = this_prod_data[this_year][1]
            this_market = vintage(this_prod_data,this_lifetime,this_in_use,repaint_freq=this_repaint_freq, weibull=self.if_weibull)
            
            this_year_vintage = this_market.vintage_for_year(this_year_prod, year)
            
            self.vintage_results_for_one_year[each_mak] = this_year_vintage 
        return self.vintage_results_for_one_year
    
    def vintage_of_a_year(self,market_vintage,year=40):
        '''
        test 
        
        Show the vintage releases of a single year break down by market sector
        '''
        year_dict = {}
        for each_mak, each_val in market_vintage.iteritems():
            this_dict={}
            this_in_use = market_vintage[each_mak]['In Use'][year]
            this_EoF = market_vintage[each_mak]['End of Life'][year]
            this_stock = market_vintage[each_mak]['Stock'][year]
            this_dict['In Use'] = this_in_use
            this_dict['End of Life'] = this_EoF
            this_dict['Stock'] = this_stock
            year_dict[each_mak] = this_dict 
        return year_dict
    
    def tot_releases_year(self):
        '''
        A getter function to calculate the total releases across year
        '''
        assert self.market_vintage_results is not None
        tot_release = 0
        for each_mak, each_val in self.market_vintage_results.iteritems():
            this_tot_release = each_val['In Use']+ each_val['End of Life']
            tot_release += this_tot_release
        return tot_release

    def to_dataframe(self,market_vintage):
        '''
        Convert the nested dictionary results to pandas dataframes
        '''
        market = []
        release_val = []
        for each_mak, each_val in market_vintage.iteritems():
            market.append(each_mak)
            release_val.append(pd.DataFrame.from_dict(each_val, orient='index'))
        df = pd.concat(release_val,keys=market)
        df.columns = np.arange(self.years[0],self.years[-1]+1)
        return df
        
    def plot_market_vintage(self,args='Total Release'):
        '''
        Function to plot out the vintage results by markets
        This verion is going to plot out graph depending on the input arguments
        
        Total Release (defult): will plot out the total release (end of life + in use) for each market
        End of Life: will plot out the end of life release for each market
        '''
        color=iter(cm.Set1(np.linspace(0,1,7)))
        if args == 'Total Release':
            fig,ax = plt.subplots(1)
            for each_mak, each_val in self.market_vintage_results.iteritems():
                c=next(color)
                this_tot_release = each_val['Manufacturing Release']+each_val['In Use']+ each_val['End of Life']
                ax.plot(self.years, this_tot_release,label = each_mak, linewidth = 2.5,c=c)
            
            #order legend
            handles, labels = ax.get_legend_handles_labels()
            handles = [handles[6],handles[0],handles[2],handles[3],handles[4],handles[5],handles[1]]
            labels = [labels[6], labels[0], labels[2],labels[3],labels[4],labels[5],labels[1]]
            ax.legend(handles,labels,loc='upper left')
            plt.xlabel('Year', fontsize=20, fontweight='bold')
            plt.ylabel('Total Releases in Tons', fontsize=20, fontweight='bold')
            plt.tick_params(labelsize=14)
            plt.show()
            
        elif args =='End of Life':
            plt.figure()
            for each_mak, each_val in self.market_vintage_results.iteritems():
                plt.plot(self.years, each_val['End of Life'],label = each_mak)
            plt.legend(loc ='upper left')
            plt.xlabel('Year', fontsize=20, fontweight='bold')
            plt.ylabel('End of Life Releases in Tonnes', fontsize=20, fontweight='bold')
            plt.show()
        elif args =='In Use':
            plt.figure()
            for each_mak, each_val in self.market_vintage_results.iteritems():
                plt.plot(self.years, each_val['In Use'],label = each_mak)
            plt.legend(loc ='upper left')
            plt.xlabel('Year', fontsize=20, fontweight='bold')
            plt.ylabel('In Use Releases in Tonnes', fontsize=20, fontweight='bold')
            plt.show()
             
       
class vintage:
    '''
    A vintage model to calculate the cumulative 
    In use and end-of-life release
    for one nano material 
    
    FOR A SINGLE MARKET
    
    The input file must be the annual production data
    The first column is the year and the second column is the production in ton
    '''
    def __init__(self, production_data, average_lifetime, in_use_release, repaint_freq=5, manufacturing_release=0.02, weibull=True):
        self.prod_data = production_data
        self.apply_to_market = self.prod_data.copy() # to keep track the change of repainting

        self.in_use_rate = float(in_use_release) #assume 10% in use release of this material
        
        self.manu_release = manufacturing_release # the amount that being released during manufacturing 
        self.repaint_freq = int(repaint_freq)
        
        self.year = self.prod_data[:,0]
        self.year_production = self.prod_data[:,1]
        
        self.num_year = len(self.year)
        self.shape = 5.0 # The shape parameter for weibull distribution, fixed to 5 at this time. Need to know why later
        self.x = self._lifetime_to_beta(float(average_lifetime)) # The average lifetime for the weibull distribution. Fixed at this time
        
        self.start_year = self.prod_data[0,0]
        self.end_year = self.prod_data[-1,0]
        
        self.if_weibull = weibull
        
    def _inUse(self, stock_last, in_use_release_rate):
        '''
        Calculate the in use release of a year 
        base on the stock size of the year before it.
        '''
        return stock_last * in_use_release_rate
    
    def _manu_release(self, prod_year, manu_release_rate):
        '''
        calculate the manufacturing release based on the production of this year
        '''
        return (prod_year/(1-manu_release_rate)) - prod_year
    
    def vintage_for_year(self, data_of_year, year):
        '''
        calculate the vintage for a single year through all the year 
        after it
        Input
            data_of_year: the production volunme of the year of this vintage (MT)
            year: what year is this vintage year?
            example: vintage_for_year(382, 1970) 
        
        Return
            A dictionary that contain the Stock size, the In use release and the end of life release 
            of this vintage in each following year.
            Any year before this year are all zeros
        ''' 
        number_of_year = year-self.start_year
        left_year = int(self.end_year - year)
        
        year_in_use = np.zeros(self.num_year)
        year_end_of_life = np.zeros(self.num_year)
        year_manu = np.zeros(self.num_year)
        year_stock = np.zeros(self.num_year)
        
        # in use release during application, assume 10% release during the first time of application
        in_use_during_app = data_of_year * 0.1

        init_stock = data_of_year * (1-0.1) # This is the initial stock size, plus the in use release
        year_stock[number_of_year] = init_stock # initialization
        year_manu[number_of_year] = in_use_during_app # the first in use release happened at the first year
       
        repaint_counter = 0 # count if this year is a repainting year
        
        for this_year in range(int(year), int(self.end_year)):
            
            year_count = this_year - int(year)
   
            i = int(this_year - self.start_year)
            i = int(i+1) # starting from the next year after the init year
            repaint_counter += 1 

            # this years in use release 
            this_in_use = year_stock[i-1] * self.in_use_rate 
            
            ''' weibull here '''
            if self.if_weibull:
                this_weibull = self.weib(year_count, self.x, self.shape) # This is the probability that it goes to end of life at this year (i)
            else: 
                this_weibull = self.static_release(year_count, self.x)
            
            this_end_of_life = year_stock[i-1] * (1-self.in_use_rate) * this_weibull
  
            this_total_release = this_in_use + this_end_of_life
            
            year_in_use[i] = this_in_use
            year_end_of_life[i] = this_end_of_life
            year_stock[i] = year_stock[i-1] - this_total_release
                   
            # if this is the repaint year:
            if repaint_counter == self.repaint_freq:
                
                repaint_counter = 0 # reset the repaint counter
                # the total in use release since the last repaint
                this_period_in_use_loss = year_in_use[i-self.repaint_freq: i]
                
                # this is the amount need to be reintroduced by the new year's production
                this_period_in_use_loss = sum(this_period_in_use_loss)
                
                year_stock[i] += this_period_in_use_loss
                
                # reduce the corresponding year's production amount
                self.apply_to_market[i,1] -= this_period_in_use_loss
                
        year_dict = {'In Use':year_in_use,"End of Life":year_end_of_life,"Manufacturing Release":year_manu,"Stock":year_stock}
   
        return year_dict
    
    def calculate_vintage(self):
        '''
        Aggregate the vintage results (In_use, end_of_life and stock size) of every vintage year
        '''
        self.total_vintage = {} # dictionary to every vintage
        
        acc_stock = np.zeros(self.num_year)
        acc_in_use_release = np.zeros(self.num_year)
        acc_end_of_life_release = np.zeros(self.num_year)
        acc_manu_release = np.zeros(self.num_year)
        acc_year_production = np.zeros(self.num_year)
        
        for i in range(int(self.num_year)):
            this_year = int(self.prod_data[i,0])
            
            this_year_production_data = self.prod_data[i,1]
            this_year_into_market_data = self.apply_to_market[i,1] 
            
            this_year_vintage = self.vintage_for_year(this_year_into_market_data, this_year)

            # add this year vintage to the total vintage dictionary, so that we can query each individual vintage later
            self.total_vintage[this_year] = this_year_vintage
            
            # accumulate the stock size
            acc_stock += this_year_vintage['Stock']
#             acc_stock[str(this_year)] = acc_stock.get(this_year,0) + this_year_vintage['Stock']
            # accumulate the in_use_release
            acc_in_use_release += this_year_vintage['In Use']
#             acc_in_use_release[str(this_year)] = acc_in_use_release.get(this_year,0) + this_year_vintage['In Use']
            # ...the end_of_life
            acc_end_of_life_release += this_year_vintage['End of Life']
#             acc_end_of_life_release[str(this_year)] = acc_end_of_life_release.get(this_year,0) + this_year_vintage['End of Life']
            
            # ...the manufacturing release
            this_manufacturing_release = self._manu_release(this_year_production_data, self.manu_release)
            acc_manu_release[i] = this_manufacturing_release
            
            acc_year_production[i] = this_year_production_data
        self.acc_vintage ={'Stock':acc_stock, 
                           'In Use':acc_in_use_release,
                           'End of Life':acc_end_of_life_release, 
                           'Manufacturing Release':acc_manu_release,
                           'Production':acc_year_production}
        
        return self.acc_vintage
    
    
    def static_release(self,x,n):
        '''
        static distribution function for the static model.
        return 1 when x == n
        return 0 otherwise
        '''
        if int(x) == int(n):
            return 1
        else:
            return 0 
        
    def weib(self,x,n,a):
        '''
        A weibull distribution generator
        X: year
        n: average lifetime in this case
        a: shape parameter
        Source: http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.weibull.html
        '''
        return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)
    
    def _lifetime_to_beta(self,average_lifetime):
        '''
        convert average lifetime to beta in Weibull distribution
        '''
        return average_lifetime/(np.exp(gammaln(1+1/self.shape)))

    def plot_vintage(self):
        '''
        A function that plot the total production, 
        the in use and end-of-life release and the stock size of each year
        '''
        assert self.acc_vintage is not None
        plt.figure()
        plt.plot(self.year,self.year_production,label='Total Production')
        plt.plot(self.year,self.acc_vintage['In Use'],label='In Use Release')
        plt.plot(self.year,self.acc_vintage['End of Life'],label='End of Life Release')
        plt.legend(loc='upper left')
        plt.show()
    
if __name__ == '__main__':
    # test
    pass
    