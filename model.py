# 导入所需的库
import gurobipy
import akshare as ak
import scipy
from gurobipy import *
import  database
import numpy as np
import pandas as pd
# 五支股票指数
stocks=["000300","399001","399006","000688","000016"]
# 五支债券指数
bonds=["sh000016","sz399307","sh000139","sh000061"]
# 根据用户输入的期望收益率和参考交易日数据计算股票债券投资比重
def caculate(day,profit):
    columns=stocks+bonds
    # 存储股票和债券数据，九列
    df = pd.DataFrame(columns=columns)
    # 从数据库获得用户输入的交易日内的五支股票指数数据
    for stock in stocks:
        data=database.read_sql("SELECT * FROM `mysystem`.`{}`ORDER BY `日期` DESC LIMIT {}".format("index"+stock,day))\
            .sort_values(by=['日期'],axis=0,ascending=True)
        df[stock]=data['收盘'].values
    # 从数据库获得用户输入的交易日内的四支债券指数数据
    for bond in bonds:
        data = database.read_sql("SELECT * FROM `mysystem`.`{}`ORDER BY `date` DESC LIMIT {}".format( bond, day))\
            .sort_values(by=['date'],axis=0,ascending=True)
        df[bond] = data['close'].values
    # 计算一日的收益率
    returns = np.log(df / df.shift(1))
    # 计算年收益率
    year_return=np.array(((df.iloc[-1,:]-df.iloc[0:1,:])/df.iloc[0:1,:])/day*252)
    # 计算九支证券的协方差矩阵
    cov=np.array(returns.cov()*252)
    #使用gurobi建模
    MODEL=gurobipy.Model()
    # 设置投资比重变量，股票和债券
    x=MODEL.addVars(range(1,len(stocks)+1),lb=0,ub=1,vtype=gurobipy.GRB.CONTINUOUS,name="stock")
    y=MODEL.addVars(range(1,len(bonds)+1),lb=0,ub=1,vtype=gurobipy.GRB.CONTINUOUS,name="bond")
    MODEL.update()
    weidht_D=gurobipy.MVar.fromlist([x[1],x[2],x[3],x[4],x[5],y[1],y[2],y[3],y[4]])
    # 设置目标函数最小化投资风险
    MODEL.setObjective(cov@weidht_D.T@weidht_D,gurobipy.GRB.MINIMIZE)
    # 设置约束，投资比重非负。
    MODEL.addConstr(x.sum()+y.sum()==1,name="weight")
    #证券收益率大于等于用户期望收益率
    MODEL.addConstr(year_return@weidht_D.T >= profit,name="profit")
    MODEL.optimize()
    Vars=[]
    for var in MODEL.getVars():
        Vars.append(var.x)
    return sum(Vars[5:])