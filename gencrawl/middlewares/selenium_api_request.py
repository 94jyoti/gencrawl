import json
from scrapy.http import HtmlResponse
from gencrawl.settings import SELENIUM_URL
from gencrawl.middlewares.selenium_request import GenSeleniumRequest
from gencrawl.util.statics import Statics


class GenSeleniumApiMiddleware():

    def process_request(self, request, spider):
        # if request is not a Selenium request, don't use this middleware
        if not isinstance(request, GenSeleniumRequest):
            return
        # to explicitly avoid using this middleware
        if request.meta.get('dont_selenium'):
            return

        data = {
            "xurl": request.url,
            "xxpath": "",
            "xcon": "",
            "load_method": "selenium"
        }
        headers = {
            'Content-Type': 'Application/Json'
        }
        meta = request.meta
        # proxy not required for Pankaj's api
        meta['dont_proxy'] = True
        # to avoid repeated request loop
        meta['dont_selenium'] = True
        meta['_selenium_original_url'] = request.url
        request = request.replace(url=SELENIUM_URL, method='POST', headers=headers, body=json.dumps(data), meta=meta,
                                  dont_filter=True)
        return request

    def process_response(self, request, response, spider):
        if not isinstance(request, GenSeleniumRequest):
            return response
        original_url = request.meta.get('_selenium_original_url')
        if not original_url:
            return response
        del request.meta['dont_selenium']
        del request.meta['dont_proxy']
        del request.meta['_selenium_original_url']

        request = request.replace(url=original_url)
        try:
            body = response.json()['html']
            body = str.encode(body)
            status = Statics.RESPONSE_CODE_OK
        except:
            body = Statics.MESSAGE_SELENIUM_FAIL
            status = Statics.RESPONSE_CODE_SELENIUM_FAIL
        return HtmlResponse(
            original_url,
            status=status,
            body=body,
            encoding=Statics.ENCODING_DEFAULT,
            request=request,
        )
