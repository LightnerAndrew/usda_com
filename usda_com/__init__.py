
'''
USDA_COM - API Wrapper for USDA Commodity Data 
===============================================

'''

import pandas as pd 
import requests 
import pkg_resources


class query(object): 
    '''
    :attr api_key: the API key given by the USDA site after creating a login. See the following link to access the code: https://apps.fas.usda.gov/psdonline/app/index.html#/app/about
    :type api_key: str
    :attr world: whether to use the Commodities or World Database 
    :type world: bool 
    
    '''


    # parameters 
    api_key = 'code'
    world = False 

    # select indicators 
    com_selection = []
    year_selection = []

    # define the source mapping 
    DATA_PATH = pkg_resources.resource_filename('usda_com', 'data/raw/')
    
    print(DATA_PATH)

    #commodity_options = pd.read_excel('../data/raw/commodities.xlsx')


    def find_commodity_code(self, search:str): 
        '''
        find codes and commodities of interest. 
        
        :param search_text: text within the commodity name. 
        :type search_text: str. 

        return 
            dataframe()
        '''

        return self.commodity_options.loc[self.commodity_options['Commodity Name'].str.contains(search_text), :]

    def run(self): 
        '''
        Run the query, return the dataframe from the USDA. 

        >>> query.run()
        '''

        base_url = 'https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/GetCommodityDataByYear'

        results = []

        for y_index, y_selection in enumerate(self.year_selection): 

            for c_index, c_selection in enumerate(self.com_selection): 
                
                # generate the new function 
                new_string = '?commodityCode = {} & marketYear = {}'.format(c_selection, y_selection)
                response = requests.get(base_url+new_string, auth=(self.api_key))

                # generate the pandas dataframe
                json = response.json()['data']
                
                results.append(json)
                

        return_data = pd.DataFrame.from_records(results)

        return return_data




    
        
