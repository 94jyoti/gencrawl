import json
import os

from datetime import datetime as dt
import psycopg2
import requests
from io import BytesIO
import pandas as pd
import sys
#from utility import Utility
cdir = os.path.join(os.getcwd().split("gencrawl")[0], 'gencrawl')
sys.path.append(cdir)
from Untitled.gencrawl.bin.google_sheet_config_setup_v3 import *
from Untitled.gencrawl.settings import CONFIG_DIR, SPIDER_DIR


def modify_final_values(json_data):
    #keys = ['phone_as_item', 'fax_as_item', 'practice_as_item']
    print("json....",json_data)
    if(json_data==None):
        spider=""
        return spider
    spider = json_data["spider"]
    '''
    for key, value in json_data.get("ext_codes").items():
        if key in keys and value and spider == 'financial_detail':
            spider = 'financial_detail_field_as_item'
            json_data['spider'] = spider
            break
    '''

    for field, value in json_data.get("ext_codes").items():
        value["name"] = field
        keys = {'paths': [], 'cleanup_functions': [], 'parsing_type': "xpath",
                'return_type': "str", 'selector': 'root', 'child_return_strategy': None}
        for key, val in keys.items():
            if key not in value:
                value[key] = val

    keys = {'domain': 'financial', 'crawl_type': 'detail', 'country': 'US', 'language': 'EN',
            'crawl_method': 'scrapy_get', 'parsing_type': "xpath", 'proxy': 'CRAWLERA(US)',
            'spider': 'financial_detail', 'start_urls': [],
            "decision_tags": {}, 'allowed_domains': [], "custom_settings": {}}

    for key, val in keys.items():
        if key not in json_data:
            if key == 'allowed_domains':
                json_data[key] = Utility.get_allowed_domains(json_data['website'])
            else:
                json_data[key] = val

    return spider


def load_to_db():
    """
    :return: loads the preset google sheet data to db
    """

    # get the data from google sheet
    google_sheet_link = "https://docs.google.com/spreadsheets/d/1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw/export?format=csv&id=1jnhZlAxHDAfBXoy6kZu9SQsdsNY-BarKx4G7t2wy7aw&gid=1108971848"
    response = requests.get(google_sheet_link)
    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    df = df.set_index('field_names', drop=True).T
    df = df.reset_index()
    #df.to_csv("test_config_dhc.csv")
    websites = df['Config'].tolist()
    print("line 61",websites)
    # spiders = df['Spider'].tolist()
    websites_without_nan = [x for x in websites if str(x) != 'nan']

    # get the json data
    gc = GoogleConfig()
    print("gcccccc",gc)
    config_dir = r'/tmp/util'
    print("websitessss without nanaannnn",websites_without_nan)
    count=1

    for web in websites_without_nan:
        if(count==2):
            break
        count=count+1
        decision_tags_list = {}
        # web_index = websites.index(web)
        json_data = gc.main(web, config_dir, 'DEVELOPMENT')
        json_data={"website":"www.americanbeaconfunds.com","spider":"financial_detail","domain":"financial","crawl_method":"SCRAPY_GET","allowed_domains":["www.americanbeaconfunds.com"],"parsing_type":"xpath","country":"US","language":"ENGLISH","start_urls":["https://www.americanbeaconfunds.com/mutual_funds/TwentyFourShortTerm.aspx"],"ext_codes":{"investment_objective":{"paths":["//*[contains(text(), 'Investment Objective')]//following-sibling::p//text()"],"return_type":"join"},"instrument_name":{"paths":["//div[@id='main']//h2//text()"],"return_type":"join"},"temp_class_blocks":{"paths":["//table[@id='grdSymbols']//tr[position()>1]"],"return_type":"selector","child_return_strategy":"multiple_items"},"share_class":{"paths":["./td[1]/text()"],"selector":"temp_class_blocks"},"nasdaq_ticker":{"paths":["./td[2]/text()"],"selector":"temp_class_blocks"},"effective_duration_date":{"paths":["//*[contains(text(), 'Portfolio info')]//span//text()"]},"temp_cusip_blocks":{"paths":["//*[contains(text(), 'TOTAL RETURNS')]//following-sibling::table//tr[position()>1]"],"return_type":"selector","child_return_strategy":"multiple_objects"},"share_class_1":{"paths":[".//td[1]/text()"],"selector":"temp_cusip_blocks"},"share_inception_date":{"paths":[".//td[2]/text()"],"selector":"temp_cusip_blocks"},"cusip":{"paths":[".//td[3]/text()"],"selector":"temp_cusip_blocks"},"cusip_1":{"paths":[".//td[4]//text()"],"selector":"temp_cusip_blocks"},"benchmarks":{"paths":["//table[@id='grdBenchmarks']//tr//td[1]//text()"],"return_type":"list"},"temp_expense_ratio_blocks":{"paths":["//*[contains(text(), 'Expense Ratios')]//following-sibling::div[1]//table//tr[position()>1]"],"return_type":"selector","child_return_strategy":"multiple_objects"},"expense_ratios_share_class":{"paths":[".//td[1]//text()"],"selector":"temp_expense_ratio_blocks"},"total_expense_gross":{"paths":[".//td[2]//span//text()"],"selector":"temp_expense_ratio_blocks"},"total_expense_net":{"paths":[".//td[3]//span//text()"],"selector":"temp_expense_ratio_blocks"},"temp_sec_yield_30":{"paths":["//*[contains(text(), 'SEC 30-Day')]//following-sibling::div//table//tr[position()>1]","//*[contains(text(), 'SEC 30-DAY')]//following-sibling::div//table//tr[position()>1]"],"return_type":"selector","child_return_strategy":"multiple_objects"},"sec_30_share_class":{"paths":[".//td[1]//text()",".//td[1]//b//text()"],"selector":"temp_sec_yield_30"},"sec_yield_30_day_actual":{"paths":[".//td[2]//span//text()",".//td[2]//b//text()"],"selector":"temp_sec_yield_30"},"sec_yield_30_day_unsubsidized":{"paths":[".//td[3]//span//text()",".//td[3]//b//text()"],"selector":"temp_sec_yield_30"},"effective_duration":{"paths":["//*[contains(text(), 'Effective Duration')]//following-sibling::td//text()"]},"average_weighted_maturity":{"paths":["//*[contains(text(), 'Effective Maturity')]//following-sibling::td//text()"]},"temp_fund_managers":{"paths":["//strong[contains(text(), 'Portfolio  Managers')]//parent::p//following-sibling::ul[position()=1]//li//text()","//strong[contains(text(),'Portfolio  Manager')]//parent::p//following-sibling::ul[position()=1]//li//text()"],"return_type":"list"},"portfolio_assets":{"paths":["//h3[contains(text(),'Total Fund')]//parent::div//span//text()"]},"portfolio_assets_date":{"paths":["//h6[contains(text(),'Portfolio information')]//span//text()"]},"sub_advisor":{"paths":["//h3[contains(text(),'Sub-Advisor')]//parent::div//td[1]//text()"],"return_type":"list"},"investment_strategy":{"paths":["//h3[contains(text(), 'Investment Strategy')]//following::ul[1]/li//text()"],"return_type":"list","cleanup_functions":["str(' '.join(obj.get('investment_strategy')))"]}}}
        print("json data after dcmain",json_data)
        json_data['pg_id']=gc.create_pg_id(json_data['website'])

        spider = modify_final_values(json_data)
        print("after passing through spider json data is in form",spider)
        if spider=="":
            print("emptyspider")
        if 'decision_tags' in json_data:
            decision_tags = json_data['decision_tags']
            if decision_tags:
                decision_tags_list = '{' + ', '.join([key.strip() for key in decision_tags.keys()]) + '}'

        json_final = json.dumps(json_data)
        json_final = json_final.replace("'", "''")
        column_name_and_values = {'id': json_data['pg_id'],
                                  'mongo_id': None,
                                  'website': json_data['website'],
                                  'domain': 'financial',
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
        print("final json format to include in dbbbbbb----------------------------")
        print(json_data)
        user = 'postgres'
        password = 'Forage2021'
        host = 'forage-dev-db.cod4levdfbtz.ap-south-1.rds.amazonaws.com'
        port = 5432
        database = 'gencrawl'
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
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


