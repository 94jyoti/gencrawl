# -*- coding: utf-8 -*-
import os
from gencrawl.util.statics import Statics

BOT_NAME = 'gencrawl'
SPIDER_MODULES = ['gencrawl.spiders']
NEWSPIDER_MODULE = 'gencrawl.spiders'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'X-Crawlera-Profile': 'desktop',
    'X-Crawlera-Cookies': 'disable'
}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 4

COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [400, 405, 500, 502, 503, 504, 520, 522, 524, 408, 403, 429]

# proxy settings
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = 'd1d3dfa7dc4444a88a253a0263be5877'


DOWNLOADER_MIDDLEWARES = {
    # engine
    'gencrawl.middlewares.retry_middleware.CustomRetryMiddleware': 540,
    'gencrawl.middlewares.pc_middleware.PCMiddleware': 545,
    'gencrawl.middlewares.selenium_api_request.GenSeleniumApiMiddleware': 551,
    'scrapy_crawlera.CrawleraMiddleware': 610,
    # 'gencrawl.middlewares.selenium_request.GenSeleniumMiddleware': 800,
    # website
}
SELENIUM_URL = "http://xpathexractoralb-516078059.ap-south-1.elb.amazonaws.com/api/xvfy/procx"
# SELENIUM_DRIVER_NAME = Statics.CHROME_SELENIUM_DRIVER
# SELENIUM_DRIVER_EXECUTABLE_PATH = os.path.join(os.getcwd(), "chromedriver")
# SELENIUM_DRIVER_ARGUMENTS = ['--no-sandbox', '--headless']


ITEM_PIPELINES = {
    'gencrawl.pipelines.validation_pipeline.ValidationPipeline': 449,
    'gencrawl.pipelines.dupefilter_pipeline.DupeFilterPipeline': 450,
    'gencrawl.pipelines.db_pipeline.DBPipeline': 500
}

# encoding
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'DEBUG'

# cache settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [400, 403, 404, 405, 408, 429, 500, 502, 503, 504, 520, 522, 524]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# directories
CONFIG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs')
RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res')
SPIDER_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'spiders')

# environment
if os.environ.get('ENVIRONMENT') == Statics.ENV_PROD:
    ENVIRONMENT = Statics.ENV_PROD
else:
    ENVIRONMENT = Statics.ENV_DEV

# dupefilter settings
ITEM_DUPEFILTER_ENABLED = True
DHC_DUPEFILTER_FIELDS = ["website", "npi", "raw_full_name", "doctor_url", "speciality", "affiliation", "practice_name",
                         "address", "phone", "fax", "email"]
NFN_DUPEFILTER_FIELDS = []

ITEM_VALIDATION_ENABLED = True
VALIDATION_FIELDS = ["website", "crawl_datetime", "http_status", "job_id", "gencrawl_id"]
DHC_VALIDATION_FIELDS = ['raw_full_name']
NFN_VALIDATION_FIELDS = []

# db settings
DB_PIPELINE_ENABLED = True
DB_BATCH_SIZE = 100

NFN_DB_USER = 'postgres'
NFN_DB_PASS = 'kapow123'
NFN_DB_HOST = '65.2.58.32'
NFN_DB_PORT = '5432'
NFN_DB_NAME = 'postgres'
NFN_CHECK_PC_TABLE = False

DHC_DB_USER = 'devuser'
DHC_DB_PASS = 'Dev#forage!2021'
DHC_DB_HOST = 'forage-dev-db.cod4levdfbtz.ap-south-1.rds.amazonaws.com'
DHC_DB_PORT = '5432'
DHC_DB_NAME = 'dhc'
DHC_CHECK_PC_TABLE = True

GENCRAWL_DB_USER = 'postgres'
GENCRAWL_DB_PASS = 'kapow123'
GENCRAWL_DB_HOST = '65.2.58.32'
GENCRAWL_DB_PORT = '5432'
GENCRAWL_DB_NAME = 'gencrawl'

