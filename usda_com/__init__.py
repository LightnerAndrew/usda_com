
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
    year_selection = 'range:range or year1,year2'



    # define the source mapping 
    DATA_PATH = pkg_resources.resource_filename('usda_com')
    commodity_options = pd.read_excel(DATA_PATH+'commodities.xlsx')
    commodity_options.columns = [col.strip() for col in commodity_options.columns]

    def find_commodity_code(self, search_text:str): 
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

        >>> query.year_selection = '1980:2000' 
        >>> query.com_selection = ['574000']
        >>> query.run()

        '''

        def to_str(i:int)->str:
            ''' turn an integer into a string '''
            return str(i)

        # generate the year list 
        def clean_years(years:str)-> list:

            if ':' in years: 
                start_year = int(years[:4]) 
                end_year = int(years[5:])
                years_range = list(map(to_str, range(start_year, end_year+1)))
            else: 
                years_range = years.split(',')
            
            return years_range

        years_range = clean_years(self.year_selection) 


        if self.world ==True: 
            world_string = 'World'
        else: 
            world_string = ''


        results = []

        for y_index, y_selection in enumerate(years_range):

            for c_index, c_selection in enumerate(self.com_selection): 
                
                # add leading zeros to 
                c_code = '0'*(7-len(c_selection))+c_selection

                headers = {
                    'Accept': 'application/json',
                    'API_KEY': self.api_key,
                }

                params = (
                    ('commodityCode', c_code),
                    ('marketYear', y_selection),
                )


                link = 'https://apps.fas.usda.gov/PSDOnlineDataServices/api/CommodityData/Get{}CommodityDataByYear'.format(world_string)

                response = requests.get(link, headers=headers, params=params)

                # generate the pandas dataframe
                json_r = response.json()

                results += json_r
                

        return_data = pd.DataFrame.from_records(results)

        return return_data




if __name__ =='__init__': 
    usda_com = query()
    
        
