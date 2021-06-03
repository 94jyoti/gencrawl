class Statics:
    # domain and crawl type constants
    DOMAIN_FINANCIAL = 'financial'
    CRAWL_TYPE_DETAIL = 'detail'
    CRAWL_TYPE_LISTING = 'listing'

    # url keys
    URL_KEY_FINANCIAL_DETAIL = "fund_url"
    URL_KEY_FINANCIAL_LISTING = "url"

    # return types
    RETURN_TYPE_DEFAULT = 'str'
    RETURN_TYPE_STRING = 'str'
    RETURN_TYPE_INT = 'int'
    RETURN_TYPE_JSON = 'json'
    RETURN_TYPE_LIST = 'list'
    RETURN_TYPE_JOIN = 'join'
    RETURN_TYPE_SELECTOR = 'selector'
    RETURN_TYPE_SELECTOR_JSON = 'selector-json'

    # PARSING types
    PARSING_TYPE_DEFAULT = 'xpath'
    PARSING_TYPE_XPATH = 'xpath'
    PARSING_TYPE_JPATH = 'jpath'
    PARSING_TYPE_REGEX = 'regex'

    # SELECTOR TYPES
    SELECTOR_DEFAULT = 'root'
    SELECTOR_ROOT = 'root'

    # other contants
    TEMP_FIELD_PREFIX = 'temp_'
    CONFIG_EXT = '.json'
    MAX_OTHER_FIELDS_LENGTH = 1000

    # filepaths
    PROJECT_DIR = 'gencrawl'
    RES_DIR = 'res'
    SITE_CONFIG_DIR = 'configs'

    # selenium settings
    CHROME_SELENIUM_DRIVER = 'chrome'
    WAIT_TIME_DEFAULT = 3

    # crawl methods
    CRAWL_METHOD_DEFAULT = 'SCRAPY_GET'
    CRAWL_METHOD_GET = "SCRAPY_GET"
    CRAWL_METHOD_POST = "SCRAPY_POST"
    CRAWL_METHOD_SELENIUM = "SELENIUM"

    # return strategy
    RETURN_STRATEGY_DEFAULT = 'multiple_objects'
    RETURN_STRATEGY_SINGLE_OBJECT = 'single_object'
    RETURN_STRATEGY_MULTIPLE_OBJECTS = 'multiple_objects'
    RETURN_STRATEGY_SINGLE_ITEM = 'single_item'
    RETURN_STRATEGY_MULTIPLE_ITEMS = 'multiple_items'

    # ignore list
    IGNORE_META_FIELDS = ['download_timeout', 'dont_proxy', 'download_slot', 'download_latency', 'depth', 'driver',
                          'selector', 'proxy']
    IGNORE_INPUT_FIELDS = ['temp_fields', 'http_status', 'job_id', 'crawl_datetime']

    # messages
    RETRY_CONDITION_MSG = "RETRY_CONDITION_MATCHED"


