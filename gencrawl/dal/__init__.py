# database access layer
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String,Boolean, MetaData, ForeignKey, DateTime
from sqlalchemy.sql import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import false
from functools import lru_cache

DeclarativeBase = declarative_base()

def get_sqlite_engine():
	return create_engine('sqlite:///sec.db')

def get_pg_engine():
	return create_engine('postgresql+psycopg2://postgres:kapow123@65.2.58.32/postgres',pool_use_lifo=True, pool_pre_ping=True, pool_recycle=3600)

def get_session(engine):
	Session = sessionmaker(bind=engine)
	return Session()

def close_session(session):
	session.close()

def db_urls(domain):
	pg_session = get_session(get_pg_engine())
	pg_engine = get_pg_engine()
	table = [x[0] for x in pg_engine.execute("select fund_url FROM public.nfn_fundlist where fund_domain like '%%"+str(domain)+"'")]
	return table
