import math
import numpy as np
import pandas as pd
import os, sys
import colorama
from colorama import Fore
import logging
logger = logging.getLogger(__name__)


class Qleaning:
    def __init__(self):
        self.shapee = []
        self.df = pd.DataFrame()
        self.filesize = ''
        self.shapee = []
        self.num_cols = []
        self.null_values = {}
        self.data_types = {}
        self.final_data_types = {}
        self.duplicates = 0
        self.final_data = {}
    
    def data_cleaning(self):
        self.read_file()
        self.check_file()
        self.file_size()
        self.dataframe_shape()
        self.check_duplicates()
        self.column_dataType_validation()
        self.fetch_column_details()
        self.generate_summary()

    def read_file(self):
        file_path = input("Enter File Path: ")
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path, engine='python')
        elif ((file_path.endswith('.xlsx')) or (file_path.endswith('.xls'))):
            sheet_name = input("Enter Sheet Name: ")
            if sheet_name == '':
                self.df = pd.read_excel(file_path)
            else: 
                self.df = pd.read_excel(file_path, sheet_name = sheet_name)
        else:
            print('Wrong File Path')
            sys.exit(-1)
    
    def check_file(self):
        if(self.df.empty):
            print("Mentioned file doesn't contain any data!!")
            sys.exit(-1)

    def file_size(self):
        logger.info("Calculating File size...")
        self.filesize = convert_size(self.df.size) #convert_size(self.dataframe.memory_usage().sum())

    def dataframe_shape(self):
        logger.info("Counting Rows and Columns...")
        self.shapee = list(self.df.shape)
    
    def check_duplicates(self):
        logger.info("Checking count of duplicate values")
        self.duplicates = self.df.duplicated(keep=False).sum()

    def column_dataType_validation(self): 
        logger.info("Column DataType Validation...")
        dlist = {'object': 'Categorical Columns', 'int32': 'Numerical Columns', 'int64': 'Numerical Columns', 'float32': 'Decimal Columns', 'float64': 'Decimal Columns', 'bool': 'Boolean Columns', 'time': 'DateTime Columns', 'date': 'DateTime Columns', 'other': 'Others'}
        col_names = np.array(list(self.df.dtypes.keys()))
        datatypes = np.array(list(self.df.dtypes.values))

        for c in list(set(datatypes)):
            if str(c) in list(dlist.keys()):
                indexs = np.where(datatypes == c)[0].tolist()
                self.data_types[dlist[str(c)]] = list(col_names[indexs])
            else:
                indexs = np.where(datatypes == c)[0].tolist()
                if 'Others' not in self.data_types:
                    self.data_types["Others"] = list(col_names[indexs])
                else:
                    self.data_types["Others"].append(list(col_names[indexs]))
    
    def fetch_column_details(self):
        columns = list(self.df.columns)
        numerics = ['int','int16', 'int32', 'int64', 'float' ,'float16', 'float32', 'float64']
        category = ['object', 'str']
        
        for c in columns:
            details = {}
            details['Null Values'] = self.df[c].isna().sum()
            if self.df[c].dtype in numerics:
                details['Minimum'] = self.df[c].min()
                details['Mean'] = self.df[c].mean()
                details['Median'] = self.df[c].median()
                details['Mode'] = self.df[c].mode()[0]
                details['Maximum'] = self.df[c].max()
                
            elif self.df[c].dtype in category:
                details['Mode'] = self.df[c].mode()[0]
                details['Count of Unique Values'] = self.df[c].nunique()
                details['Unique Values'] = list(self.df[c].unique())[:5]
            
            self.final_data[c] = details
            


    def generate_summary(self):
        logger.info("Generating Results...")
        print("-------------------------------------------------------------------------------")
        print("File size                           : " + str(self.filesize))
        print("Total No. of Rows                   : " + str(self.shapee[0]))
        print("Total No. of Columns                : " + str(self.shapee[1]))
        print("Count of Duplicate records          : "  + str(self.duplicates))
        print("_______________________________________________________________________________")
        print("Count of Data types                 : ") 
        print("--------------------------------------") 
        for k, va in self.data_types.items():
            print("                                     "+k+ " -> " + str(len(va)))
        print("_______________________________________________________________________________")
        print()
        print("Column Details                      : ") 
        print("--------------------------------------") 
        c=1
        for k, va in self.final_data.items():
            print(Fore.YELLOW +str(c)+"."+k, ": "+ Fore.RESET)
            c+=1
            for x, y in va.items():
                print("                   >", x, "-", y)
            print()
        print("_______________________________________________________________________________")




def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
