import json
import os
from google_sheet_config_setup_v3 import *
from datetime import datetime as dt
import psycopg2


def modify_final_values(json_data):
    keys = ['phone_as_item', 'fax_as_item', 'practice_as_item']
    spider = json_data["spider"]
    for key, value in json_data.get("ext_codes").items():
        if key in keys and value and spider == 'hospital_detail':
            print(f"Changing spider name for - {json_data.get('website')}")
            spider = 'hospital_detail_field_as_item'
            json_data['spider'] = spider
            break
    return spider


def load_to_db():
    """
    :return: loads the preset google sheet data to db
    """
    # get the data from google sheet
    google_sheet_link = "https://docs.google.com/spreadsheets/u/1/d/1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw/export?format=csv&id=1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw&gid=1934331278"
    response = requests.get(google_sheet_link)
    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    df = df.set_index('field_names', drop=True).T
    df = df.reset_index()
    websites = df['Config'].tolist()
    # spiders = df['Spider'].tolist()
    websites_without_nan = [x for x in websites if str(x) != 'nan']

    # get the json data
    gc = GoogleConfig()
    config_dir = r'/tmp/util'

    for web in websites_without_nan:
        decision_tags_list = {}
        # web_index = websites.index(web)
        json_data = gc.main(web, config_dir, 'DEVELOPMENT')
        spider = modify_final_values(json_data)
        if 'decision_tags' in json_data:
            decision_tags = json_data['decision_tags']
            if decision_tags:
                decision_tags_list = '{' + ', '.join([key.strip() for key in decision_tags.keys()]) + '}'

        json_final = json.dumps(json_data)
        json_final = json_final.replace("'", "''")
        column_name_and_values = {'id': json_data['pg_id'],
                                  'mongo_id': None,
                                  'website': json_data['website'],
                                  'domain': 'hospital',
                                  'crawl_type': 'detail',
                                  'country': json_data['country'],
                                  'language': json_data['language'],
                                  'spider': spider,
                                  'tagged_by': '',
                                  'dev': '',
                                  'created_at': dt.now(),
                                  'updated_at': dt.now(),
                                  'tag_hours': 0,
                                  'dev_hours': 0,
                                  'updated_hours': 0,
                                  'is_partial': False,
                                  'search_tags': decision_tags_list,
                                  'config': json_data
                                  }
        # columns_names = ', '.join([key for key in column_name_and_values.keys()])
        # column_values = ', '.join(["'" + str(value) + "'" for value in column_name_and_values.values()])
        # table_name = 'websites'
        # connect and upload to db
        user = 'postgres'
        password = 'kapow123'
        host = '65.2.58.32'
        port = 5432
        database = 'gencrawl'
        try:
            connection = psycopg2.connect(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)

            cursor = connection.cursor()
            sql_insert_statement = """INSERT INTO public.websites
            (id, mongo_id, website, "domain", crawl_type, country, "language", spider, tagged_by, dev, created_at, updated_at, tag_hours, dev_hours, update_tag_hours, update_dev_hours, is_partial, search_tags, config)
            VALUES('{}', NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '', now(), now(), 0, 0, 0, 0, false, '{}', '{}');
            """.format(column_name_and_values['id'],
                       column_name_and_values['website'],
                       column_name_and_values['domain'],
                       column_name_and_values['crawl_type'],
                       column_name_and_values['country'],
                       column_name_and_values['language'],
                       column_name_and_values['spider'],
                       column_name_and_values['tagged_by'],
                       decision_tags_list,
                       json_final)
            cursor.execute(sql_insert_statement)
            connection.commit()
            count = cursor.rowcount
        except Exception as error:
            print(str(error))
            print("Error in read/update operation: " + str(error))
        else:
            pass
        finally:
            # closing database connection.
            # noinspection PyUnboundLocalVariable
            if connection:
                cursor.close()
                connection.close()


if __name__ == '__main__':
    load_to_db()
