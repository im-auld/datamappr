import json
import urllib
import urllib2
from multiprocessing import Process, Value
import time
import os
from os.path import isdir
from os.path import isfile
from os import listdir
import zipfile

from pandas import DataFrame, date_range, read_csv, read_excel, concat, isnull, ExcelWriter
import csv
import pandas as pd
import datetime
import numpy as np

base_url = 'http://research.stlouisfed.org'
process_num = 5
processes = {}
data_folder = 'rawdata'

data_dict = {'coincident_index':'PHCI',
            'leading_index':'SLIND',
            'nonfarm_payrolls':'NA',
            'unemployment_rate':'UR',
            'real_GDP':'NGSP',
            'housing_starts':'BP1FHSA',
            'resident_population':'POP',
            'labor_force':'LF',
            'initial_claims':'ICLAIMS',
            'personal_income':'OTOT',
            'assets_commercial_banks':'QATA',
            'house_price_index':'STHPI'
            }
data_dict2 = {'hourly_earnings':'S\M\U\0\1\0\SMU01000000500000003SA',
             'weekly_hours':'S\M\U\0\1\0\SMU01000000500000002SA'
            }  
state_dict = {
        'AL':	'Alabama',
        'AK':	'Alaska',
        'AZ':	'Arizona',
        'AR':	'Arkansas',
        'CA':	'California',
        'CO':	'Colorado',
        'CT':	'Connecticut',
        'DE':	'Delaware',
        'FL':	'Florida',
        'GA':	'Georgia',
        'HI':	'Hawaii',
        'ID':	'Idaho',
        'IL':	'Illinois',
        'IN':	'Indiana',
        'IA':	'Iowa',
        'KS':	'Kansas',
        'KY':	'Kentucky',
        'LA':	'Louisiana',
        'ME':	'Maine',
        'MD':	'Maryland',
        'MA':	'Massachusetts',
        'MI':	'Michigan',
        'MN':	'Minnesota',
        'MS':	'Mississippi',
        'MO':	'Missouri',
        'MT':	'Montana',
        'NE':	'Nebraska',
        'NV':	'Nevada',
        'NH':	'New Hampshire',
        'NJ':	'New Jersey',
        'NM':	'New Mexico',
        'NY':	'New York',
        'NC':	'North Carolina',
        'ND':	'North Dakota',
        'OH':	'Ohio',
        'OK':	'Oklahoma',
        'OR':	'Oregon',
        'PA':	'Pennsylvania',
        'RI':	'Rhode Island',
        'SC':	'South Carolina',
        'SD':	'South Dakota',
        'TN':	'Tennessee',
        'TX':	'Texas',
        'UT':	'Utah',
        'VT':	'Vermont',
        'VA':	'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI':	'Wisconsin',
        'WY': 'Wyoming',
        }

fips_dict = {
        'AL'	:	1,
        'AK'	:	2,
        'AZ'	:	4,
        'AR'	:	5,
        'CA'	:	6,
        'CO'	:	8,
        'CT'	:	9,
        'DE'	:	10,
        'DC'	:	11,
        'FL'	:	12,
        'GA'	:	13,
        'HI'  :	15,
        'ID'  :	16,
        'IL'	:	17,
        'IN'	:	18,
        'IA'	:	19,
        'KS'	:	20,
        'KY'	:	21,
        'LA'	:	22,
        'ME'	:	23,
        'MD'	:	24,
        'MA'	:	25,
        'MI'	:	26,
        'MN'	:	27,
        'MS'	:	28,
        'MO'	:	29,
        'MT'	:	30,
        'NE'	:	31,
        'NV'	:	32,
        'NH'	:	33,
        'NJ'	:	34,
        'NM'	:	35,
        'NY'	:	36,
        'NC'	:	37,
        'ND'	:	38,
        'OH'	:	39,
        'OK'	:	40,
        'OR'	:	41,
        'PA'	:	42,
        'RI'	:	44,
        'SC'	:	45,
        'SD'	:	46,
        'TN'	:	47,
        'TX'	:	48,
        'UT'	:	49,
        'VT'	:	50,
        'VA'	:	51,
        'WA'	:	53,
        'WV'	:	54,
        'WI'	:	55,
        'WY'	:	56,
        }

def test_func():
    print 'hello'

def activate_dl_process(data_shredder):
    for index, data in enumerate(data_shredder):
        print index
        processes['dl{}'.format(index)] = Process(target=download_data, args=(data,))
    for process in processes:
        processes[process].start()
    for process in processes:
        processes[process].join()
        
def data_collection():
    with open('govdata/datafiles.json', 'r') as file:
        json_data = file.read()
    dataset = json.loads(json_data)
    data_shredder = []
    count = len(dataset)
    divisor = count/process_num
    for x in range(0,process_num):
        data_shredder.append(dataset[x*divisor:(x+1)*divisor],)
        if x==process_num-1:
            data_shredder.append(dataset[(x+1)*divisor:])
    activate_dl_process(data_shredder)

def download_data(dataset):
    for data in dataset:
        url = base_url+data['link'][0]
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(data_folder+'/'+file_name, 'wb')
        meta = u.info()
        file_size = 1500000
        #USE THIS WHEN HEADER INFORMATION IS AVAILABLE
        #file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl*100.0/file_size)
            print status
        #print 'Downloading '+data['state']+' data...'
        #THIS IS THE SIMPLER WAY WITHOUT PROGRESS STATUS
        #urllib.urlretrieve(base_url + data['link'][0], data_folder+'/'+data['state']+'.zip')
        f.close()

def unzip_files(all_files):
    root_directory = os.getcwd()+'/'+data_folder
    for zipped_file in all_files:
        extract_file = zipfile.ZipFile(root_directory+'/'+zipped_file)
        extract_file.extractall(root_directory)

def file_check(all_files, state_short, keys):

    def help_file_check(curr_directory):
        if isdir(curr_directory):
            for file in listdir(curr_directory):
                if state_short+data_dict[keys]+'.csv' in file:
                    return curr_directory+'/'+file
                elif state_short+data_dict[keys] in file:
                    return curr_directory+'/'+file
                elif data_dict[keys]+'.csv' in file:
                    return curr_directory+'/'+file
                elif data_dict[keys] in file:
                    return curr_directory+'/'+file
        #print 'Attempt on '+curr_directory+' for '+state_dict[state_short]+'failed'
        #print data_dict[keys]
        #print logic_list
        return None

    logic_list = ['',
                '/'+state_short[1],
                '/'+state_dict[state_short][1].upper(),
                '/'+state_short[1]+'/'+data_dict[keys][0],
                '/'+state_dict[state_short][1].upper()+'/'+data_dict[keys][0],
                '']

    reset = all_files
    while logic_list:
        curr_directory = reset
        curr_directory = curr_directory+logic_list.pop(0)
        checker = help_file_check(curr_directory)
        if checker != None:
            break 
    if not logic_list:
        print 'File Not Found!'
        print reset
        raise ValueError
    return checker
  
if __name__ == '__main__':
    test_dir = data_folder+'/STIL_csv_2.zip'
    if not isfile(test_dir) and not isdir(test_dir):
        print 'Collecting Data...'
        data_collection()
        #download_data([{"state": "Illinois",
                    #"link": ["/fred2/categories/27290/downloaddata/STIL_csv_2.zip"]}])
    else:
        print 'Data Present'               
        all_files = listdir(data_folder)
        unzip_test_dir = test_dir[:-4]
        if not isfile(unzip_test_dir) and not isdir(unzip_test_dir):
            unzip_files(all_files)

        unzipped_dirs = []
        for file in all_files:
            if '.zip' not in file:
                unzipped_dirs.append(file)

    for index, metric in enumerate(data_dict):
        df_state = []
        for index, unzipped_dir in enumerate(unzipped_dirs):
            state_short = unzipped_dir[2:4]
            files_root = data_folder+'/'+unzipped_dir+'/data'
            if isdir(files_root+'/'+state_short[0]):
                filename = file_check(files_root+'/'+state_short[0],state_short,metric)
            else:
                filename = file_check(files_root,state_short,metric)
            df_state.append(read_csv(filename))
            df_state[index].columns = ['date', 'value']
            df_state[index]['state'] = state_short
            mask = pd.Series([item!='.' for item in df_state[index]['value']], index=df_state[index].index)
            df_state[index]= df_state[index][mask]
        print 'Generating DataFrame for '+metric
        df_result = pd.tools.merge.concat(df_state,axis=0)
        df_result.to_csv('cleandata/'+metric+'.csv')


""" 
        df_master = []
        for index, unzipped_dir in enumerate(unzipped_dirs):
            df_join={}
            state_short = unzipped_dir[2:4]
            files_root = data_folder+'/'+unzipped_dir+'/data'
            for index, keys in enumerate(data_dict): 
                if isdir(files_root+'/'+state_short[0]):
                    filename = file_check(files_root+'/'+state_short[0],state_short,keys)
                else:
                    filename = file_check(files_root,state_short,keys)

                df_join['dataframe{}'.format(index)] = read_csv(filename)
                df_join['dataframe{}'.format(index)].columns=[keys+' date', keys+' value']
        
            df_state = df_join['dataframe0']
            del df_join['dataframe0']
            for dataframe in df_join:
                df_state = df_state.join(df_join[dataframe], how='outer')
            df_state['state'] = state_short
            df_master.append(df_state)

        df_result = pd.tools.merge.concat(df_master,axis=0)
        xlsfile = 'df_result_test.xlsx'
        df.to_csv(xlsfile)
"""
        