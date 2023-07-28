from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.types import VARCHAR,INTEGER,FLOAT
import configuration as config
import datetime
today=(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y%m%d")
DTYPES={'ts_code':VARCHAR(10),"trade_date":INTEGER,"open":FLOAT,"high":FLOAT,"low":FLOAT, "close":FLOAT,"pre_close":FLOAT, "change":FLOAT,"pct_chg":FLOAT,"vol":FLOAT,"amount":FLOAT}
engine_ts = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'
                          .format(config.user,config.password,config.host,config.port,config.db))
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine_ts))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import models.model
    Base.metadata.create_all(bind=engine_ts)


def write_data(name,df,DTYPES):
    res = df.to_sql(name, engine_ts, index=False, if_exists='append', chunksize=7000,dtype=DTYPES)

def write_data_notypes(name,df):
     res=df.to_sql(name, engine_ts, index=False, if_exists='append', chunksize=7000)

def read_sql(sql):
    df = pd.read_sql_query(text(sql), engine_ts.connect())
    return df


def read_data(code):
    sql = "SELECT * FROM `mysystem`.`{}` ".format(code)
    df = pd.read_sql_query(text(sql), engine_ts.connect())
    return df


def get_data(stock_code,start_date,end_date=today):
    pro = config.pro
    df = pro.query('daily', ts_code=stock_code, start_date=start_date, end_date=end_date)\
        .sort_values(by=['trade_date'],axis=0,ascending=True)
    return df


def update_data(table):
    sql="SELECT * FROM `mysystem`.`{}` ORDER BY `TRADE_DATE` DESC LIMIT 1".format(table)
    df = pd.read_sql_query(text(sql), engine_ts.connect())
    print(df)
    print(str(df['ts_code'].values),str(df['trade_date'].values))
    newdf =get_data(stock_code=str(df['ts_code'].values[0]), start_date=str(df['trade_date'].values[0]), end_date=today)
    print(newdf)
    write_data(table, newdf,DTYPES=DTYPES)



