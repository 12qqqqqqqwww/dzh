from sqlalchemy import desc
import news as nw
import model
from model import *
import database
from database import *
from models.model import *
from flask import Flask
from flask_cors import CORS
from flask import Flask, jsonify, request, json,render_template
app = Flask(__name__)
CORS(app)
#添加了dzh
startdate="20230201"
@app.route('/getuserbyid/<string:uid>',methods=['GET', 'POST'])
def getUser(uid):
    user=Adm.query.filter(Adm.name==uid).first()
    data={ 'adm_ID':user.name,'adm_Psd':user.psd}
    return data

@app.route('/getnews',methods=['GET', 'POST'])
def getNews():
    news=News.query.order_by(desc(News.id)).all()
    data=[]
    for news in news:
        data.append({ 'title':str(news.title),'content':news.content,'link':news.link})
    return data


@app.route("/getStock/<string:code>",methods=['GET', 'POST'])
def getStock(code):
    data=[]
    metadata = MetaData()
    # 从数据库中反射表结构
    metadata.reflect(bind=engine_ts)
    # 获取所有表的名称
    table_names = metadata.tables.keys()
    # 打印所有表的名称
    if code in table_names:
        update_data(code)
        stock=read_data(code).iloc[1:, 1:6]
        for idx, idata in stock.iterrows():
            data.append(
                {"date": idata["trade_date"], "open": idata['open'], "close": idata['close'], "low": idata['low'],
                 "high": idata['high']})
        return jsonify(data)
    else:
        stockid = Stock.query.filter(Stock.symbol == code).first().ts_code
        df = get_data(stockid,startdate)
        write_data(code, df,database.DTYPES)
        stock = read_data(code).iloc[1:, 1:6]
        for idx, idata in stock.iterrows():
            data.append(
                {"date": idata["trade_date"], "open": idata['open'], "close": idata['close'], "low": idata['low'],
                 "high": idata['high']})
        return jsonify(data)



@app.route("/getStockList",methods=['GET', 'POST'])
def getStockList():
    data=[]
    stock=Stock.query.filter().all
    for stock in stock():
        data.append({"symbol":stock.symbol,"area":stock.area,"name":stock.name,"industry":stock.industry,"list_date":stock.list_date})
    return jsonify(data)

@app.route("/getweight/<int:day>/<int:profit>",methods=['GET', 'POST'])
def getweight(day,profit):
    try:
        bond=model.caculate(day,profit/100)
        return {"bond":bond}
    except:
        return {"bond":2}

@app.route("/addCollect",methods=['GET', 'POST'])
def add():
    data = json.loads(request.get_data())
    u=User(data['name'],data['stock'])
    db_session.add(u)
    db_session.commit()
    return {"status":200}


@app.route("/getstock/<string:username>",methods=['GET'])
def getstock(username):
    data=[]
    user=User.query.filter(User.name==username).all
    for u in user():
        stock=Stock.query.filter(Stock.symbol==u.stock).first()
        data.append({"symbol":stock.symbol,"area":stock.area,"name":stock.name,"industry":stock.industry,"list_date":stock.list_date})
    return jsonify(data)


@app.route("/delCollect/<string:stock>/<string:username>",methods=['GET', 'POST'])
def delstock(stock,username):
    user = User.query.filter(User.stock == stock ,User.name==username).first()
    db_session.delete(user)
    db_session.commit()
    return {"status":200}


@app.route("/delnew",methods=[ 'POST'])
def delnew():
    data = json.loads(request.get_data())
    new=News.query.filter(News.link==data['link']).first()
    db_session.delete(new)
    db_session.commit()
    return {"status":200}


@app.route("/updatenew",methods=[ 'POST'])
def updatenewnew():
    database.write_data_notypes('news', nw.getNews())
    return {"status":200}


@app.route("/addnew",methods=[ 'POST'])
def addnew():
    data = json.loads(request.get_data())
    new=News(title=data['title'],link=data['link'],content=data['content'])
    db_session.add(new)
    db_session.commit()
    return {"status":200}


@app.route("/addqes",methods=[ 'POST'])
def addqes():
    data = json.loads(request.get_data())
    qs=Questions(data['content'])
    db_session.add(qs)
    db_session.commit()
    return {"status":200}


@app.route("/getqes",methods=[ 'GET'])
def getqes():
    qs=Questions.query.all()
    data=[]
    for u in qs:
        data.append({'qes_ID':u.Id,"qes_content":u.content})
    return jsonify(data)

@app.route("/editstocklist",methods=['POST'])
def editstock():
    data = json.loads(request.get_data())
    stock=Stock.query.filter(Stock.symbol==data['symbol']).first()
    stock.name=data['name']
    stock.area=data['area']
    stock.industry=data['industry']
    stock.list_date=data['list_date']
    db_session.commit()
    return {"status":200}



@app.route("/delstocklist",methods=[ 'POST'])
def delstocklist():
    data = json.loads(request.get_data())
    stock = Stock.query.filter(Stock.symbol == data['symbol']).first()
    db_session.delete(stock)
    db_session.commit()
    return {"status":200}

@app.route("/addstocklist",methods=['POST'])
def addstock():
    data = json.loads(request.get_data())
    s=Stock(ts_code=data['ts_code'],name=data['name'],area=data['area'],
            industry=data['industry'],list_date=data['list_date'],symbol=data['symbol'])
    db_session.add(s)
    db_session.commit()
    return {"status":200}

if __name__ == '__main__':
    app.run(debug=True)
