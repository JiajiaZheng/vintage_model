'''
Created on Nov 23, 2016

@author: rsong_admin
'''
import pandas as pd
import numpy as np
from collections import OrderedDict


def draw_full_sankey(tio2,sio2,feox):
    '''
    return the csv file to draw the full sankey diagram
    '''
    pass

def draw_detailed_sankey(tio2,sio2,feox, year=2016.0):
    '''
    return the csv file to draw the detailed sankey diagram
    '''
    last_year = str(year - 1)
    year = str(year)
    
    # define structure here
    final_dict = {('TiO2 in Stock (all uses)','Household & Furniture'):[0],
                  ('TiO2 in Stock (all uses)','Automotive'):[0],
                  ('TiO2 in Stock (all uses)','Medical'):[0],
                  ('TiO2 in Stock (all uses)','Other Industries'):[0],
                  ('TiO2 in Stock (all uses)','Packaging'):[0],
                  ('TiO2 in Stock (all uses)','Electronics'):[0],
                  ('TiO2 in Stock (all uses)','Construction & Building'):[0],
                  ('SiO2','Household & Furniture'):[0],
                  ('SiO2','Automotive'):[0],
                  ('SiO2','Medical'):[0],
                  ('SiO2','Other Industries'):[0],
                  ('SiO2','Packaging'):[0],
                  ('SiO2','Electronics'):[0],
                  ('SiO2','Construction & Building'):[0],
                  ('FeOx','Household & Furniture'):[0],
                  ('FeOx','Automotive'):[0],
                  ('FeOx','Medical'):[0],
                  ('FeOx','Other Industries'):[0],
                  ('FeOx','Packaging'):[0],
                  ('FeOx','Electronics'):[0],
                  ('FeOx','Construction & Building'):[0],
                  ('Household & Furniture','In Use Release'):[0],
                  ('Automotive','In Use Release'):[0],
                  ('Medical','In Use Release'):[0],
                  ('Other Industries','In Use Release'):[0],
                  ('Packaging','In Use Release'):[0],
                  ('Electronics','In Use Release'):[0],
                  ('Construction & Building','In Use Release'):[0],
                  ('Household & Furniture','End of Life Release'):[0],
                  ('Automotive','End of Life Release'):[0],
                  ('Medical','End of Life Release'):[0],
                  ('Other Industries','End of Life Release'):[0],
                  ('Packaging','End of Life Release'):[0],
                  ('Electronics','End of Life Release'):[0],
                  ('Construction & Building','End of Life Release'):[0]
                  }
    
    # pack value here
    
    # TiO2 Stock to Household & Furniture
    tio2_stk_to_House = tio2[year].loc['Household & Furniture']['In Use'] + tio2[year].loc['Household & Furniture']['End of Life']
    final_dict[('TiO2 in Stock (all uses)','Household & Furniture')] = [tio2_stk_to_House]
    
    # TiO2 Stock to Automotive:
    tio2_stk_to_Auto = tio2[year].loc['Automotive']['In Use'] + tio2[year].loc['Automotive']['End of Life']
    final_dict[('TiO2 in Stock (all uses)','Automotive')] = [tio2_stk_to_Auto]
    
    # TiO2 Stock to Medical
    tio2_stk_to_Medical = tio2[year].loc['Medical']['In Use'] + tio2[year].loc['Medical']['End of Life']
    final_dict[('TiO2 in Stock (all uses)','Medical')] = [tio2_stk_to_Medical]
    
    # TiO2 Stock to Other Industries
    tio2_stk_to_Other = tio2[year].loc['Other Industries']['In Use'] + tio2[year].loc['Other Industries']['End of Life']
    final_dict[('TiO2 in Stock (all uses)','Other Industries')] = [tio2_stk_to_Other]
    
    # TiO2 Stock to Packaging
    tio2_stk_to_Packaging = tio2[year].loc['Packaging']['In Use'] + tio2[year].loc['Packaging']['End of Life']
    final_dict[('TiO2 in Stock (all uses)','Packaging')] = [tio2_stk_to_Packaging]
    
    # TiO2 Stock to Electronics
    tio2_stk_to_Electronics = tio2[year].loc['Electronics']['In Use'] + tio2[year].loc['Electronics']['End of Life']
    final_dict[('TiO2 in Stock (all uses)','Electronics')] = [tio2_stk_to_Electronics]
    
    # TiO2 Stock to Electronics
    tio2_stk_to_Construc = tio2[year].loc['Construction & Building']['In Use'] + tio2[year].loc['Construction & Building']['End of Life']
    final_dict[('TiO2 in Stock (all uses)','Construction & Building')] = [tio2_stk_to_Construc]
    
    # sio2 Stock to Household & Furniture
    sio2_stk_to_House = sio2[year].loc['Household & Furniture']['In Use'] + sio2[year].loc['Household & Furniture']['End of Life']
    final_dict[('SiO2','Household & Furniture')] = [sio2_stk_to_House]
    
    # siO2 Stock to Automotive:
    sio2_stk_to_Auto = sio2[year].loc['Automotive']['In Use'] + sio2[year].loc['Automotive']['End of Life']
    final_dict[('SiO2','Automotive')] = [sio2_stk_to_Auto]
    
    # sio2 Stock to Medical
    sio2_stk_to_Medical = sio2[year].loc['Medical']['In Use'] + sio2[year].loc['Medical']['End of Life']
    final_dict[('SiO2','Medical')] = [sio2_stk_to_Medical]
    
    # sio2 Stock to Other Industries
    sio2_stk_to_Other = sio2[year].loc['Other Industries']['In Use'] + sio2[year].loc['Other Industries']['End of Life']
    final_dict[('SiO2','Other Industries')] = [sio2_stk_to_Other]
    
    # sio2 Stock to Packaging
    sio2_stk_to_Packaging = sio2[year].loc['Packaging']['In Use'] + sio2[year].loc['Packaging']['End of Life']
    final_dict[('SiO2','Packaging')] = [sio2_stk_to_Packaging]
    
    # sio2 Stock to Electronics
    sio2_stk_to_Electronics = sio2[year].loc['Electronics']['In Use'] + sio2[year].loc['Electronics']['End of Life']
    final_dict[('SiO2','Electronics')] = [sio2_stk_to_Electronics]
    
    # sio2 Stock to Electronics
    sio2_stk_to_Construc = sio2[year].loc['Construction & Building']['In Use'] + sio2[year].loc['Construction & Building']['End of Life']
    final_dict[('SiO2','Construction & Building')] = [sio2_stk_to_Construc]
    
    # feox Stock to Household & Furniture
    feox_stk_to_House = feox[year].loc['Household & Furniture']['In Use'] + feox[year].loc['Household & Furniture']['End of Life']
    final_dict[('FeOx','Household & Furniture')] = [feox_stk_to_House]
    
    # feox Stock to Automotive:
    feox_stk_to_Auto = feox[year].loc['Automotive']['In Use'] + feox[year].loc['Automotive']['End of Life']
    final_dict[('FeOx','Automotive')] = [feox_stk_to_Auto]
    
    # feox Stock to Medical
    feox_stk_to_Medical = feox[year].loc['Medical']['In Use'] + feox[year].loc['Medical']['End of Life']
    final_dict[('FeOx','Medical')] = [feox_stk_to_Medical]
    
    # feox Stock to Other Industries
    feox_stk_to_Other = feox[year].loc['Other Industries']['In Use'] + feox[year].loc['Other Industries']['End of Life']
    final_dict[('FeOx','Other Industries')] = [feox_stk_to_Other]
    
    # feox Stock to Packaging
    feox_stk_to_Packaging = feox[year].loc['Packaging']['In Use'] + feox[year].loc['Packaging']['End of Life']
    final_dict[('FeOx','Packaging')] = [feox_stk_to_Packaging]
    
    # feox Stock to Electronics
    feox_stk_to_Electronics = feox[year].loc['Electronics']['In Use'] + feox[year].loc['Electronics']['End of Life']
    final_dict[('FeOx','Electronics')] = [feox_stk_to_Electronics]
    
    # feox Stock to Electronics
    feox_stk_to_Construc = feox[year].loc['Construction & Building']['In Use'] + feox[year].loc['Construction & Building']['End of Life']
    final_dict[('FeOx','Construction & Building')] = [feox_stk_to_Construc]
    
    # House to In use Release
    House_to_in_use_release = tio2[year].loc['Household & Furniture']['In Use'] \
                              + sio2[year].loc['Household & Furniture']['In Use']\
                              + tio2[year].loc['Household & Furniture']['In Use']
    final_dict[('Household & Furniture','In Use Release')] = [House_to_in_use_release]
    
    # Auto to In use Release
    Automotive_to_in_use_release = tio2[year].loc['Automotive']['In Use'] \
                              + sio2[year].loc['Automotive']['In Use']\
                              + tio2[year].loc['Automotive']['In Use']
    final_dict[('Automotive','In Use Release')] = [Automotive_to_in_use_release]
    
    # Medical to In use Release
    Medical_to_in_use_release = tio2[year].loc['Medical']['In Use'] \
                              + sio2[year].loc['Medical']['In Use']\
                              + tio2[year].loc['Medical']['In Use']
    final_dict[('Medical','In Use Release')] = [Medical_to_in_use_release]
    
    # Other Industries to In use Release
    Other_to_in_use_release = tio2[year].loc['Other Industries']['In Use'] \
                              + sio2[year].loc['Other Industries']['In Use']\
                              + tio2[year].loc['Other Industries']['In Use']
    final_dict[('Other Industries','In Use Release')] = [Other_to_in_use_release]
    
    # Packaging to In use Release
    Packaging_to_in_use_release = tio2[year].loc['Packaging']['In Use'] \
                              + sio2[year].loc['Packaging']['In Use']\
                              + tio2[year].loc['Packaging']['In Use']
    final_dict[('Packaging','In Use Release')] = [Packaging_to_in_use_release]
    
    # Construction & Building to In use Release
    Construct_to_in_use_release = tio2[year].loc['Construction & Building']['In Use'] \
                              + sio2[year].loc['Construction & Building']['In Use']\
                              + tio2[year].loc['Construction & Building']['In Use']
    final_dict[('Construction & Building','In Use Release')] = [Construct_to_in_use_release]
    
    # Electronics to In use Release
    Electronics_to_in_use_release = tio2[year].loc['Electronics']['In Use'] \
                              + sio2[year].loc['Electronics']['In Use']\
                              + tio2[year].loc['Electronics']['In Use']
    final_dict[('Electronics','In Use Release')] = [Electronics_to_in_use_release]
    
    #####
    
    # House to End of Life Release
    House_to_in_use_release = tio2[year].loc['Household & Furniture']['End of Life'] \
                              + sio2[year].loc['Household & Furniture']['End of Life']\
                              + tio2[year].loc['Household & Furniture']['End of Life']
    final_dict[('Household & Furniture','End of Life Release')] = [House_to_in_use_release]
    
    # Auto to End of Life Release
    Automotive_to_in_use_release = tio2[year].loc['Automotive']['End of Life'] \
                              + sio2[year].loc['Automotive']['End of Life']\
                              + tio2[year].loc['Automotive']['End of Life']
    final_dict[('Automotive','End of Life Release')] = [Automotive_to_in_use_release]
    
    # Medical to End of Life Release
    Medical_to_in_use_release = tio2[year].loc['Medical']['End of Life'] \
                              + sio2[year].loc['Medical']['End of Life']\
                              + tio2[year].loc['Medical']['End of Life']
    final_dict[('Medical','End of Life Release')] = [Medical_to_in_use_release]
    
    # Other Industries to End of Life Release
    Other_to_in_use_release = tio2[year].loc['Other Industries']['End of Life'] \
                              + sio2[year].loc['Other Industries']['End of Life']\
                              + tio2[year].loc['Other Industries']['End of Life']
    final_dict[('Other Industries','End of Life Release')] = [Other_to_in_use_release]
    
    # Packaging to End of Life Release
    Packaging_to_in_use_release = tio2[year].loc['Packaging']['End of Life'] \
                              + sio2[year].loc['Packaging']['End of Life']\
                              + tio2[year].loc['Packaging']['End of Life']
    final_dict[('Packaging','End of Life Release')] = [Packaging_to_in_use_release]
    
    # Construction & Building to In use Release
    Construct_to_in_use_release = tio2[year].loc['Construction & Building']['End of Life'] \
                              + sio2[year].loc['Construction & Building']['End of Life']\
                              + tio2[year].loc['Construction & Building']['End of Life']
    final_dict[('Construction & Building','End of Life Release')] = [Construct_to_in_use_release]
    
    # Electronics to In use Release
    Electronics_to_in_use_release = tio2[year].loc['Electronics']['End of Life'] \
                              + sio2[year].loc['Electronics']['End of Life']\
                              + tio2[year].loc['Electronics']['End of Life']
    final_dict[('Electronics','End of Life Release')] = [Electronics_to_in_use_release]

    
    print final_dict
    return pd.DataFrame(final_dict)


    
if __name__ == '__main__':
    # test
    tio2_df = pd.read_csv('../results/TiO2_vintage_results.csv',index_col=[0,1])
    sio2_df = pd.read_csv('../results/SiO2_vintage_results.csv',index_col=[0,1])
    feox_df = pd.read_csv('../results/Fe_vintage_results.csv',index_col=[0,1])
    
    sankey_dataframe = draw_detailed_sankey(tio2_df, sio2_df, feox_df,year=2016.0)
    sankey_dataframe.transpose().to_csv('test.csv')