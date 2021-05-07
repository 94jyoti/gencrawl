from importlib import import_module
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from scrapy_selenium import SeleniumMiddleware
from scrapy import Request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

