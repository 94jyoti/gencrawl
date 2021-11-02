# database access layer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DAL:
	def __init__(self, settings, client):
		self.client = client
		self.engine = create_engine(
			f'postgresql+psycopg2://{settings["DB_USER"]}:{settings["DB_PASS"]}@{settings["DB_HOST"]}:{settings["DB_PORT"]}/{settings["DB_NAME"]}',
			pool_use_lifo=True, pool_pre_ping=True, pool_recycle=3600)
		self.client_input_queries = {
			"NFN": """select fund_url FROM public.nfn_fundlist where (fund_domain like '%www.{}%'
					or fund_domain like '%//{}%' or fund_domain like '{}%')""",
			"DHC": """
				SELECT distinct("DoctorUrl") FROM public.dhc_master_input_table_october_2021 where "DoctorUrl"!='' and 
				("DoctorUrl" like '%www.{}%' or "DoctorUrl" like '%//{}%' or "DoctorUrl" like '{}%') 
				"""
		}

	def create_session(self, engine):
		session = sessionmaker(bind=engine)
		return session()

	def close_session(self, session):
		session.close()

	def get_db_urls(self, domain, limit):
		limit = int(limit)
		pg_session = self.create_session(self.engine)
		query = self.client_input_queries[self.client].format(domain, domain, domain)
		if limit > 0:
			query = query + f"LIMIT {limit}"
		print(query)
		results = [x[0] for x in pg_session.execute(query)]
		self.close_session(pg_session)
		return results
