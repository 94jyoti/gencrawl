# -*- coding: utf-8 -*-
import os
from gencrawl.util.statics import Statics
#testing branches
BOT_NAME = 'gencrawl'
SPIDER_MODULES = ['gencrawl.spiders']
NEWSPIDER_MODULE = 'gencrawl.spiders'

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 4

COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [400, 500, 502, 503, 504, 520, 522, 524, 408, 403, 429]

# proxy settings
CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = 'd1d3dfa7dc4444a88a253a0263be5877'

DOWNLOADER_MIDDLEWARES = {
    # engine
    'gencrawl.middlewares.retry_middleware.CustomRetryMiddleware': 551,
    'scrapy_crawlera.CrawleraMiddleware': 610,
    'gencrawl.middlewares.selenium_request.GenSeleniumMiddleware': 800
    # website
}
SELENIUM_DRIVER_NAME = Statics.CHROME_SELENIUM_DRIVER
# SELENIUM_DRIVER_EXECUTABLE_PATH = os.path.join(os.getcwd(), "chromedriver")
SELENIUM_DRIVER_ARGUMENTS = ['--no-sandbox', '--headless']

ITEM_PIPELINES = {
      'gencrawl.pipelines.nfn_pipelines.NFNPipeline': 300,
}

# encoding
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'DEBUG'

# cache settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [400, 404, 500, 502, 503, 504, 520, 522, 524, 408, 403, 429]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# directories
CONFIG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'configs')
RES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res')
SPIDER_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'spiders')

# environment
# if job is running on zyte server
if os.environ.get('SHUB_JOBKEY') or os.environ.get('ENVIRONMENT') == Statics.ENV_PROD:
    ENVIRONMENT = Statics.ENV_PROD
else:
    ENVIRONMENT = Statics.ENV_DEV
