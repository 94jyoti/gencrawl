import os

# -*- coding: utf-8 -*-
ENVIRONMENT = 'PRODUCTION'

BOT_NAME = 'gencrawl'

SPIDER_MODULES = ['gencrawl.spiders']

NEWSPIDER_MODULE = 'gencrawl.spiders'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
DOWNLOAD_DELAY = 0
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 100

COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 8
RETRY_HTTP_CODES = [500, 502, 503, 504, 520, 522, 524, 408, 403, 429]

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}
DOWNLOADER_MIDDLEWARES = {}
ITEM_PIPELINES = {
        'gencrawl.pipelines.nfn_pipelines.NFNPipeline': 300,
}
SELENIUM_PATH = os.path.join(os.getcwd(), "chromedriver")

# encoding
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'DEBUG'

