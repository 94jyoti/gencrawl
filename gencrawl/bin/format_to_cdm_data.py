import pandas as pd
import json
import sys
import os
import numpy as np
# adding path to env variable
cdir = os.path.join(os.getcwd().split("gencrawl")[0], 'gencrawl')
sys.path.append(cdir)
#from gencrawl.settings import RES_DIR
from collections import OrderedDict
from Untitled.gencrawl.util.statics import Statics
from Untitled.gencrawl.util.utility import Utility
RES_DIR="/Users/sumitagrawal/Documents/GitHub/gencrawl/Untitled/gencrawl/res"


def explode(df, lst_cols, fill_value='', preserve_index=False):
    # make sure `lst_cols` is list-alike
    if lst_cols is not None and len(lst_cols) > 0 and not isinstance(lst_cols, (list, tuple, np.ndarray, pd.Series)):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)
    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()
    # preserve original index values    
    idx = np.repeat(df.index.values, lens)
    # create "exploded" DF
    res = (pd.DataFrame({
                col:np.repeat(df[col].values, lens)
                for col in idx_cols},
                index=idx)
             .assign(**{col:np.concatenate(df.loc[lens>0, col].values)
                            for col in lst_cols}))
    # append those rows that have empty lists
    if (lens == 0).any():
        # at least one list in cells is empty
        res = (res.append(df.loc[lens==0, idx_cols], sort=False)
                  .fillna(fill_value))
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:        
        res = res.reset_index(drop=True)
    return res




def transpose_column(column_list, df):
    column_names = list(df.head())
    for header_name in column_list:
        temp=[x for x in column_names if x.startswith(header_name)]
        df[header_name]=df[temp[0]]
        for i in range(len(temp)-1):
            df[header_name] = df[header_name].map(str) + ',' + df[temp[i + 1]].map(str)
        df = df.drop(temp, axis=1)
        df[header_name]=df[header_name].str.split(',')
        #df.assign(ex_date=df['ex_date'].str.split(',')).explode('ex_date')

    df.to_csv('abc.csv')
    df1 = explode(df=df, lst_cols=column_list, fill_value=',')
    return df1
    

if __name__ == "__main__":
    input_file = sys.argv[1]
    file_name, format = input_file.rsplit(".", 1)
    assert format in ["csv"]
    #field_mapping_file = os.path.join(RES_DIR, field_mapping_file)
    field_mapping = []


    df=pd.read_csv(input_file)
    column_names = list(df.head())
    output_columns={"Fund URL":"Domain",'Instrument Name':"Fund Name/Ticker",'Share Class':"Class Name"}
    input_coulmns=['Fund URL','Instrument Name','Share Class']
    column_list=['Record Date','Ex Date','Long Term (Per Share)','Short Term (Per Share)','Total (Per Share)']
    transpose_df = transpose_column(column_list,df)
    outputdf=transpose_df[input_coulmns + column_list]
    outputdf=outputdf.rename(columns = output_columns, inplace = False)
    outputdf["Page URL"]=outputdf["Domain"]
    outputdf = outputdf.reindex(["Domain","Page URL","Fund Name/Ticker","Record Date","Ex Date","Payble Date","Reinvest Date","Ordinary Income","ST Cap Gains","LT Cap Gains","Total Distribution","Reinvest Nav/Price","Class Name","Income/Amount/Share/Dividend","YEAR","Annual Distribution Rate* (%)","Period","Investment Income","Return of Capital","Capital Gains","Rate","Year End NAV"], axis=1)
    outputdf.to_csv('abc2.csv',index=False)