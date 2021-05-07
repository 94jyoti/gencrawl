class Statics:
    # domain and crawl type constants
    DOMAIN_FINANCIAL = 'financial'
    CRAWL_TYPE_DETAIL = 'detail'
    CRAWL_TYPE_LISTING = 'listing'

    # return types
    RETURN_TYPE_STRING = 'str'
    RETURN_TYPE_INT = 'int'
    RETURN_TYPE_JSON = 'json'
    RETURN_TYPE_LIST = 'list'
    REUTRN_TYPE_JOIN = 'join'
    RETURN_TYPE_SELECTOR = 'selector'

    # PARSING types
    PARSING_TYPE_XPATH = 'xpath'
    PARSING_TYPE_JPATH = 'jpath'
    PARSING_TYPE_REGEX = 'regex'

    DEFAULT_SELECTOR = 'root'
    CONFIG_EXT = '.json'
    SITE_CONFIG_DIR = 'configs'
    CHROME_SELENIUM_DRIVER = 'chrome'

    # crawl methods
    CRAWL_METHOD_GET = "SCRAPY_GET"
    CRAWL_METHOD_POST = "SCRAPY_POST"
    CRAWL_METHOD_SELENIUM = "SELENIUM"

    # other contants
    ROOT_SELECTOR = 'root'
    TEMP_FIELD_PREFIX = 'temp_'

    # return strategy
    RETURN_STRATEGY_SINGLE_OBJECT = 'single_object'
    RETURN_STRATEGY_MULTIPLE_OBJECTS = 'multiple_objects'
    RETURN_STRATEGY_SINGLE_ITEM = 'single_item'
    RETURN_STRATEGY_MULTIPLE_ITEMS = 'multiple_items'



