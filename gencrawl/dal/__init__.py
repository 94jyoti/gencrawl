# database access layer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DAL:
	def __init__(self, settings):
		self.engine = create_engine(
			f'postgresql+psycopg2://{settings["DB_USER"]}:{settings["DB_PASS"]}@{settings["DB_HOST"]}:{settings["DB_PORT"]}/{settings["DB_NAME"]}',
			pool_use_lifo=True, pool_pre_ping=True, pool_recycle=3600)

	def create_session(self, engine):
		session = sessionmaker(bind=engine)
		return session()

	def close_session(self, session):
		session.close()

	def get_db_urls(self, domain):
		pg_session = self.create_session(self.engine)
		results = [x[0] for x in pg_session.execute(
			"select fund_url FROM public.nfn_fundlist where fund_domain like '%%" + str(domain) + "'")]
		self.close_session(pg_session)
		return results
