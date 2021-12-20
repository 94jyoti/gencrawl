from scrapy.downloadermiddlewares.retry import RetryMiddleware
from gencrawl.util.statics import Statics


class CustomRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        do_retry = False
        if spider.retry_condition:
            ext_codes = {"retry_condition": spider.retry_condition}
            do_retry = spider.exec_codes(response, ext_codes=ext_codes)[0].get("retry_condition")
            reason = Statics.MESSAGE_RETRY_CONDITION

        if response.status == Statics.RESPONSE_CODE_PC_FAIL:
            do_retry = True
            request = request.replace(url=response.url)
            reason = Statics.MESSAGE_PC_FAIL_RETRY

        if do_retry:
            return self._retry(request, reason, spider) or response
        else:
            return response
