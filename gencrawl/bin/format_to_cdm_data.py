import pandas as pd
import json
import sys
import os
import numpy as np

# adding path to env variable
cdir = os.path.join(os.getcwd().split("gencrawl")[0], 'gencrawl')
sys.path.append(cdir)
# from gencrawl.settings import RES_DIR
from collections import OrderedDict
from Untitled.gencrawl.util.statics import Statics
from Untitled.gencrawl.util.utility import Utility

RES_DIR = "/Users/sumitagrawal/Documents/GitHub/gencrawl/Untitled/gencrawl/res"


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
    res = (pd.DataFrame({col: np.repeat(df[col].values, lens) for col in idx_cols}, index=idx).assign(
        **{col: np.concatenate(df.loc[lens > 0, col].values) for col in lst_cols}))
    # append those rows that have empty lists
    if (lens == 0).any():
        # at least one list in cells is empty
        res = (res.append(df.loc[lens == 0, idx_cols], sort=False).fillna(fill_value))
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:
        res = res.reset_index(drop=True)
    return res


def transpose_column(column_list, df,length=-1):
    column_names = list(df.head())
    print(column_list)
    flag=False
    if length == -1:
        flag =  True
    for header_name in column_list:
        temp = [x for x in column_names if x.startswith(header_name)]
        print("temp---", temp)
        df[header_name] = df[temp[0]]
        if flag:
            length=len(temp)
        for i in range(length - 1):
            try:
                print("oiiiiiiii",i)
                df[header_name] = df[header_name].map(str) + '|' + df[temp[i + 1]].map(str)
                print("inside for", df[header_name])
            except Exception as e:
                df[header_name] = df[header_name].map(str) + '|' + ''

        df = df.drop(temp, axis=1)
        df[header_name] = df[header_name].str.split('|')
        print("--------------------------------")
        print("cdjskcbdsjkcbsdjcdjkscbsdc", df[header_name])
        # for i in df['header_name']:
        #   if("nan" in i):
        #      list.remove(i)

        # df.assign(ex_date=df['ex_date'].str.split(',')).explode('ex_date')

    df.to_csv('abc.csv')
    df1 = explode(df=df, lst_cols=column_list, fill_value=',')
    print("df111", df1)
    return df1


def add_one(x):
    return x.split("com")[0] + "com/"


if __name__ == "__main__":
    input_file = sys.argv[1]
    file_name, format = input_file.rsplit(".", 1)
    assert format in ["csv"]
    # field_mapping_file = os.path.join(RES_DIR, field_mapping_file)
    field_mapping = []

    #df = pd.read_csv(input_file,converters={i: str for i in range(0, 100)})
    df = pd.read_csv(input_file, low_memory=False, dtype='unicode')
    df = df.fillna('')
    # df.drop(df.loc[df['CG Record Date 1'] == None].index, inplace=True)
    # df=df.apply(str)
    column_names = list(df.head())
    print("cdcdcd", column_names)
    # output_columns={"Fund URL":"Domain",'Instrument Name':"Fund Name/Ticker",'Share Class':"Class Name","Total (Per Share)":"Total Distribution","CG Ex Date":"Ex Date","Short Term (Per Share)":"ST Cap Gains","CG Record Date":"Record Date","Long Term (Per Share)":"LT Cap Gains","Ex Date":"Frequency" }
    '''
    output_columns = {"Fund URL": "Domain", 'Nasdaq Ticker 1': "Fund Name/Ticker", 'Share Class': "Class Name",
                      "Total (Per Share)": "Capital Gains","Reinvestment Price": "Reinvest Nav/Price", "Per Share": "Total Distribution", "Short Term (Per Share)": "ST Cap Gains",
                      "Long Term (Per Share)": "LT Cap Gains","Pay Date":"Payble Date",}
    '''
    output_columns = {"Fund URL": "Domain", 'Nasdaq Ticker': "Fund Name/Ticker", 'Share Class': "Class Name",
                      "Total (Per Share)": "Capital Gains", "Reinvestment Price": "Reinvest Nav/Price",
                      "Per Share": "Total Distribution", "Short Term (Per Share)": "ST Cap Gains",
                      "Long Term (Per Share)": "LT Cap Gains", "Pay Date": "Payble Date",'CG Reinvestment Price':"Reinvest Nav/Price","CG Record Date":"Record Date","CG Ex Date":"Ex Date","CG Pay Date":"Payble Date"}
        #,'CG Ex Date':"Ex Date","CG Record Date":"Record Date",'CG Pay Date':"Payble Date"}
    input_coulmns = ['Fund URL', 'Nasdaq Ticker','Share Class']
    # column_list=['Ex Date','Pay Date','Per Share']
    column_list = ['CG Ex Date','CG Pay Date','CG Record Date','Ordinary Income','CG Reinvestment Price','Long Term (Per Share)','Short Term (Per Share)']

    df=df.replace(np.nan, ' ')
    df=df.drop_duplicates()
    transpose_df = transpose_column(column_list, df,200)
    outputdf = transpose_df[input_coulmns + column_list]
    outputdf = outputdf.dropna(how='all', axis=0)
    outputdf = outputdf.rename(columns=output_columns, inplace=False)
    outputdf["Page URL"] = outputdf["Domain"]
    #outputdf["Reinvest Date"] = outputdf["Ex Date"]
    #outputdf = outputdf.reindex(["Domain", "Page URL", "Fund Name/Ticker", "Record Date","Ex Date", "Payble Date", "Reinvest Date","Ordinary Income", "ST Cap Gains", "LT Cap Gains","CG Record Date",'CG Pay Date','CG Ex Date',"Total Distribution", "Reinvest Nav/Price", "Class Name", "Income/Amount/Share/Dividend", "Frequency", "Annual Distribution Rate* (%)", "Period", "Investment Income","Return of Capital", "Capital Gains", "Rate", "Year End NAV"], axis=1)
    outputdf = outputdf.reindex(
        ["Domain", "Page URL", "Fund Name/Ticker", "Record Date", "Ex Date", "Payble Date", "Reinvest Date",
         "Ordinary Income","ST Cap Gains", "LT Cap Gains", "Total Distribution", "Reinvest Nav/Price", "Class Name",
         "Income/Amount/Share/Dividend", "Frequency", "Annual Distribution Rate* (%)", "Period", "Investment Income",
         "Return of Capital", "Capital Gains", "Rate", "Year End NAV"], axis=1)
    outputdf["Domain"] = outputdf["Domain"].apply(add_one)
    print(outputdf["Domain"])
    outputdf = outputdf[outputdf['Ex Date'] !='nan']
    # print("knfsklvf",type(outputdf['Ex Date'][54]))

    outputdf1 = outputdf.replace(np.nan, '')
    #outputdf1 = outputdf.replace("nan", "")
    outputdf1 = outputdf1.drop_duplicates()
    #outputdf1 = outputdf.fillna('')
    outputdf1.to_csv('lazard_distri.csv', index=False, )