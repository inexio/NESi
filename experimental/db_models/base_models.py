from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Enum, Boolean, FLOAT, Float
from sqlalchemy.ext.declarative import declarative_base as db
from sqlalchemy.orm import sessionmaker, relationship


alcatel_base = db()
huawei_base = db()
alcatel_engine = create_engine('sqlite:///alcatel.db')
huawei_engine = create_engine('sqlite:///huawei.db')
Session = sessionmaker()

