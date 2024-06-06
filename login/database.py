from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 지금은 sqlite3로 사용
SQLALCHEMY_DATABASE_URL = 'mysql://admin:qwer1234@mydatabase.cleikgoaszdk.ap-northeast-2.rds.amazonaws.com/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()