# 对获取的数据进行数据清洗操作
import numpy as np
import pandas as pd

def loadCsvToPandas(file_path="", index_col=""):
    df = pd.read_csv(file_path, index_col=index_col, header=0,parse_dates=True)
    return df


def clean(df):
    new_df = cleanAllNanColumn(df)
    new_df = cleanUnnamedColumns(new_df)
    new_df = cleanAllNotNanRow(new_df)
    return new_df

# 清洗所有Nan列
def cleanAllNanColumn(df):
    new_df = df.dropna(axis=1, how="all")
    return new_df

def cleanUnnamedColumns(df):
    return df[df.columns.drop(list(df.filter(regex="Unnamed")))]

# 选择所有非空行数据作为新的DataFrame
def cleanAllNotNanRow(df):
    new_df = df.dropna(how="any")
    return new_df

def cleanItemContain_L(df,item_name):
    if df[item_name].dtypes != 'float64':
        df = df[df[item_name].str.count("L")==0]
        df = df.astype({"溶解氧": "float64"})
    return  df

def selectColumn(df, item_name="", drop_nan=True, split_num=0):
    new_df = df[item_name]

    before_df = None
    after_df = None

    if drop_nan:
        new_df = new_df.dropna()

    if split_num > 0:
        before_df = df[:split_num]
        after_df = df[split_num:]

    return new_df, before_df, after_df

# mode lt 小于 gt 大于 between 在数值之间
def selectDataByCondition(df, item_name="", mode="lt", first_val=None, second_val=None):
    new_df = df
    if mode == "lt" and first_val != None:
        new_df = new_df[new_df[item_name] < first_val]

    elif mode == "gt" and first_val != None:
        new_df = new_df[new_df[item_name] > first_val]

    elif mode == "between" and first_val != None and second_val != None:
        new_df = new_df[(new_df[item_name] > first_val) & (new_df[item_name] < second_val)]

    return new_df