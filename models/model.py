from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    Id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name=Column(String(50))
    stock = Column(String(50))
    def __init__(self, name,stock):
        self.name = name
        self.stock=stock

class Adm(Base):
    __tablename__ = 'admers'
    __table_args__ = {'extend_existing': True}
    Id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name=Column(String(50))
    psd = Column(String(50))
    def __init__(self, name,psd):
        self.name = name
        self.psd=psd



class Questions(Base):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}
    Id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    content=Column(String(500))
    def __init__(self, content):
        self.content = content

class News(Base):
    __tablename__ = 'news'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    content = Column(String(2000))
    link = Column(String(120))

    def __init__(self, title,link,content):
        self.title=title
        self.content=content
        self.link=link
    def __repr__(self):
        return '<news %r>' % (self.title)

class Stock(Base):
    __tablename__ = 'stocks'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    ts_code=Column(String(120))
    symbol=Column(String(120))
    name=Column(String(120))
    area=Column(String(120))
    industry=Column(String(120))
    list_date=Column(String(120))

    def __init__(self,ts_code,symbol,name,area,industry,list_date):
        self.ts_code=ts_code
        self.symbol=symbol
        self.name=name
        self.area=area
        self.industry=industry
        self.list_date=list_date


    def __repr__(self):
        return '<news %r>' % (self.id)
