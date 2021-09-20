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
        res = (res.append(df.loc[lens == 0, idx_cols], sort=False)
               .fillna(fill_value))
    # revert the original index order
    res = res.sort_index()
    # reset index if requested
    if not preserve_index:
        res = res.reset_index(drop=True)
    return res


def transpose_column(column_list, df):
    column_names = list(df.head())
    print(column_list)
    for header_name in column_list:
        temp = [x for x in column_names if x.startswith(header_name)]
        print("temp---", temp)
        df[header_name] = df[temp[0]]
        for i in range(len(temp) - 1):
            print("oiiiiiiii",i)
            df[header_name] = df[header_name].map(str) + '|' + df[temp[i + 1]].map(str)
            print("inside for", df[header_name])
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

    df = pd.read_csv(input_file)
    df = df.fillna('')
    # df.drop(df.loc[df['CG Record Date 1'] == None].index, inplace=True)
    # df=df.apply(str)
    column_names = list(df.head())
    print("cdcdcd", column_names)
    # output_columns={"Fund URL":"Domain",'Instrument Name':"Fund Name/Ticker",'Share Class':"Class Name","Total (Per Share)":"Total Distribution","CG Ex Date":"Ex Date","Short Term (Per Share)":"ST Cap Gains","CG Record Date":"Record Date","Long Term (Per Share)":"LT Cap Gains","Ex Date":"Frequency" }
    output_columns = {"Fund URL": "Domain", 'Nasdaq Ticker': "Fund Name/Ticker", 'Share Class': "Class Name",
                      "Total (Per Share)": "Capital Gains", "CG Ex Date": "YEAR",
                      "Reinvestment Price": "Reinvest Nav/Price", "Per Share": "Total Distribution", "Short Term (Per Share)": "ST Cap Gains",
                      "Long Term (Per Share)": "LT Cap Gains", "CG Pay Date": "Payble Date"}
    '''
    output_columns = { "Income": "Income/Amount/Share/Dividend",
                     "Instrument Name": "Fund Name/Ticker", "Ticker": "Fund Name/Ticker",
                     "Income/Amount/Share/Dividend": "Income/Amount/Share/Dividend",
                     "Cash Amount": "Income/Amount/Share/Dividend",
                     "Cash": "Income/Amount/Share/Dividend",
                     "Amount": "Income/Amount/Share/Dividend",
                     "Ordinary Income": "Ordinary Income",
                     "Dividend Income": "Income/Amount/Share/Dividend",
                     "Distribution NAV": "Income/Amount/Share/Dividend",
                     "Income Dividends per Share ($)": "Income/Amount/Share/Dividend",
                     "Short-Term Capital Gains per Share ($)": "ST Cap Gains",
                     "ST Cap Gains": "ST Cap Gains", "SHORT TERM": "ST Cap Gains",
                     "Long-Term Capital Gains per Share ($)": "LT Cap Gains",
                     "LT Cap Gains": "LT Cap Gains",
                     "LONG TERM": "LT Cap Gains",
                     "REINVESTMENT PRICE ($)": "Reinvest Nav/Price",
                     "Reinvest Nav/Price": "Reinvest Nav/Price",
                     "Year- End NAV": "Reinvest Nav/Price",
                     "Total Distribution per Share ($)": "Total Distribution",
                     "TOTAL DISTRIBUTION": "Total Distribution",
                     "Distribution Total": "Total Distribution",
                     "Total Distribution": "Total Distribution",
                     "PER SHARE DISTRIBUTION": "Total Distribution",
                     "Ex Date": "Ex Date", "EX-DATE": "Ex Date",
                     "Payble Date": "Payble Date",
                     "Record Date": "Record Date",
                     "Reinvest Date": "Reinvest Date",
                     "Capital Gains Distribution": "Capital Gains", "Capital Gains": "Capital Gains",
                     "Class Name": "Class Name", "Investment Income": "Investment Income"
                     }
            '''
    input_coulmns = ['Fund URL', 'Nasdaq Ticker', 'Share Class']
    # column_list=['Ex Date','Pay Date','Per Share']
    column_list = ["CG Record Date","Record Date","Long Term (Per Share)","Short Term (Per Share)","Total (Per Share)","Ordinary Income"]
    print(df)
    transpose_df = transpose_column(column_list, df)
    outputdf = transpose_df[input_coulmns + column_list]
    outputdf = outputdf.dropna(how='all', axis=0)
    outputdf = outputdf.rename(columns=output_columns, inplace=False)
    outputdf["Page URL"] = outputdf["Domain"]
    outputdf = outputdf.reindex(
        ["Domain", "Page URL", "Fund Name/Ticker", "Record Date","CG Record Date","Ex Date", "Payble Date", "Reinvest Date",
         "Ordinary Income", "ST Cap Gains", "LT Cap Gains", "Total Distribution", "Reinvest Nav/Price", "Class Name",
         "Income/Amount/Share/Dividend", "Frequency", "Annual Distribution Rate* (%)", "Period", "Investment Income",
         "Return of Capital", "Capital Gains", "Rate", "Year End NAV"], axis=1)
    outputdf["Domain"] = outputdf["Domain"].apply(add_one)
    print(outputdf["Domain"])
    outputdf = outputdf[outputdf['Record Date'] !='nan']
    # print("knfsklvf",type(outputdf['Ex Date'][54]))

    outputdf1 = outputdf.replace(np.nan, '')
    outputdf1 = outputdf.replace("nan", "")
    # outputdf1 = outputdf.fillna('')
    outputdf1.to_csv('thornburg_dividend.csv', index=False, )
