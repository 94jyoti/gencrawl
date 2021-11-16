# database access layer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gencrawl.util.statics import Statics


class DAL:

	@staticmethod
	def _create_engine(settings, client):
		return create_engine(
			f'postgresql+psycopg2://{settings[f"{client}_DB_USER"]}:{settings[f"{client}_DB_PASS"]}@{settings[f"{client}_DB_HOST"]}:{settings[f"{client}_DB_PORT"]}/{settings[f"{client}_DB_NAME"]}',
			pool_use_lifo=True, pool_pre_ping=True, pool_recycle=3600)

	def __init__(self, settings, client):
		self.client = client.upper()
		self.engine = DAL._create_engine(settings, self.client)
		self.client_input_queries = {
			"NFN": """select fund_url FROM public.nfn_fundlist where (fund_domain like '%www.{}%'
					or fund_domain like '%//{}%' or fund_domain like '{}%')""",
			"DHC": """
				SELECT distinct("DoctorUrl") FROM public.dhc_master_input_table_october_2021 where "DoctorUrl"!='' and 
				("DoctorUrl" like '%www.{}%' or "DoctorUrl" like '%//{}%' or "DoctorUrl" like '{}%') 
				"""
		}

	@staticmethod
	def get_config_from_db(settings, config):
		client = Statics.CLIENT_GENCRAWL
		engine = DAL._create_engine(settings, client)
		pg_session = sessionmaker(bind=engine)()
		query = "SELECT config FROM public.websites where id = '{}'".format(config)
		results = [x[0] for x in pg_session.execute(query)]
		pg_session.close()
		if results:
			results = results[0]
		return results

	def _create_session(self, engine):
		session = sessionmaker(bind=engine)
		return session()

	def _close_session(self, session):
		session.close()

	def get_db_urls(self, domain, limit):
		limit = int(limit)
		pg_session = self._create_session(self.engine)
		query = self.client_input_queries[self.client].format(domain, domain, domain)
		if limit > 0:
			query = query + f"LIMIT {limit}"
		print(query)
		results = [x[0] for x in pg_session.execute(query)]
		self._close_session(pg_session)
		return results

