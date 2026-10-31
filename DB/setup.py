from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column,String,Text,create_engine,Integer

url="sqlite:///DB/data.db"
engine=create_engine(url)
session_local=sessionmaker(bind=engine)
base=declarative_base()


class User(base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String)
    password=Column(String)

base.metadata.create_all(engine)


def get_db():
    return session_local()
