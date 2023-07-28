import akshare as ak
import scipy
from sqlalchemy import VARCHAR, INTEGER, FLOAT,Date

import  database
import numpy as np
import pandas as pd
startdate="20180101"
stocks=["000300","399001","399006","000688","000016"]
bonds=["sh000016","sz399307","sh000139","sh000061"]
DTYPEofStock={'日期':Date,"开盘":FLOAT,"最高":FLOAT,"涨跌额":FLOAT, "最低":FLOAT,
              "收盘":FLOAT,"成交量":FLOAT, "成交额":FLOAT,"振幅":FLOAT,"涨跌幅":FLOAT,"换手率":FLOAT}
DtypeofBond={"date":Date,"open":FLOAT,"high":FLOAT,"low":FLOAT, "close":FLOAT,"volume":FLOAT}
for stock in stocks:
    stock_zh_index_daily_df = ak.index_zh_a_hist(symbol=stock, period="daily", start_date=startdate,
                                                 end_date=database.today)
    database.write_data("index"+stock,stock_zh_index_daily_df,DTYPEofStock)
for bond in bonds:
    bond_zh_index_daily_df =bond_zh_hs_daily_df = ak.bond_zh_hs_daily(symbol=bond)
    database.write_data(bond,bond_zh_index_daily_df,DtypeofBond)

