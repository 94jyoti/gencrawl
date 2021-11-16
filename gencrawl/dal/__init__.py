# database access layer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gencrawl.util.statics import Statics
from psycopg2.extras import execute_values
from psycopg2 import sql
import json


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
		self.client_insert_columns = {
			"DHC": ['job_id', 'gencrawl_id', 'profile_id', 'website', 'search_url', 'doctor_url', 'http_status',
					'unique_data_identifier', 'raw_address', 'raw_name', 'json_data']
		}
		self.client_column_mapping = {
			"DHC": {"raw_name": "raw_full_name", "raw_address": "address_raw_1"}
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

	def insert_raw_output(self, items):
		pg_session = self._create_session(self.engine)
		columns = self.client_insert_columns[self.client]
		column_mapping = self.client_column_mapping.get(self.client) or {}
		db_rows = [{k: item.get(column_mapping.get(k) or k) for k in columns} for item in items]
		for item, row in zip(items, db_rows):
			row['json_data'] = json.dumps(item).replace("'", "''")
			# TODO remove this temp check
			row['profile_id'] = 1
		connection = pg_session.bind.raw_connection()
		with connection.cursor() as cursor:
			query = sql.SQL("""INSERT INTO gencrawl_raw_output({fields}) VALUES %s;""").format(
				fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
			).as_string(cursor)
			try:
				execute_values(cur=cursor, sql=query,
							   argslist=[tuple(row.get(col) for col in columns) for row in db_rows])
				connection.commit()
			except Exception as error:
				print(str(error))
		self._close_session(pg_session)


