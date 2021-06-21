from importlib import import_module
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from scrapy_selenium import SeleniumMiddleware
from scrapy import Request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


class GenSeleniumRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self, wait_time=None, wait_until=None, screenshot=False, script=None,
                 iframe=None, *args, **kwargs):
        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script
        self.iframe = iframe
        super().__init__(*args, **kwargs)


class GenSeleniumMiddleware(SeleniumMiddleware):

    def __init__(self, driver_name, driver_executable_path, browser_executable_path,
                 command_executor, driver_arguments):
        """Initialize the selenium webdriver
        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        driver_arguments: list
            A list of arguments to initialize the driver
        browser_executable_path: str
            The path of the executable binary of the browser
        command_executor: str
            Selenium remote server endpoint
        """

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_klass_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_klass = getattr(driver_klass_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_klass = getattr(driver_options_module, 'Options')

        driver_options = driver_options_klass()

        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        for argument in driver_arguments:
            driver_options.add_argument(argument)

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        # locally installed driver
        if driver_executable_path is not None:
            driver_kwargs = {
                'executable_path': driver_executable_path,
                f'{driver_name}_options': driver_options
            }
            self.driver = driver_klass(**driver_kwargs)
        # remote driver
        elif command_executor is not None:
            from selenium import webdriver
            capabilities = driver_options.to_capabilities()
            self.driver = webdriver.Remote(command_executor=command_executor,
                                           desired_capabilities=capabilities)
        else:
            from selenium import webdriver
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=driver_options)

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get('SELENIUM_BROWSER_EXECUTABLE_PATH')
        command_executor = crawler.settings.get('SELENIUM_COMMAND_EXECUTOR')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        if driver_name is None:
            raise NotConfigured('SELENIUM_DRIVER_NAME must be set')

        # if driver_executable_path is None and command_executor is None:
        #     raise NotConfigured('Either SELENIUM_DRIVER_EXECUTABLE_PATH '
        #                         'or SELENIUM_COMMAND_EXECUTOR must be set')

        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            browser_executable_path=browser_executable_path,
            command_executor=command_executor,
            driver_arguments=driver_arguments
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    """Scrapy middleware handling the requests using selenium"""
    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""
        if not isinstance(request, GenSeleniumRequest):
            return None

        self.driver.get(request.url)
        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie(
                {
                    'name': cookie_name,
                    'value': cookie_value
                }
            )
        if request.wait_time:
            if request.wait_until:
                WebDriverWait(self.driver, request.wait_time).until(
                    EC.presence_of_element_located((By.XPATH, request.wait_until))
                )
            else:
                time.sleep(request.wait_time)

        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        if request.iframe:
            try:
                iframe = self.driver.find_element_by_xpath(request.iframe)
                if iframe:
                    self.driver.switch_to.frame(iframe)
            except:
                print(f"iframe not found - {request.iframe}")
        body = str.encode(self.driver.page_source)
        # Expose the driver via the "meta" attribute
        # request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

