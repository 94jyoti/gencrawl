from gencrawl.util.statics import Statics


class CustomRedirectMiddleware:

    def process_response(self, request, response, spider):
        if spider.retry_condition:
            ext_codes = {"retry_condition": spider.retry_condition}
            do_retry = spider.exec_codes(response, ext_codes=ext_codes)[0].get("retry_condition")
            if do_retry:
                reason = Statics.RETRY_CONDITION_MSG
                return self._retry(request, reason, spider) or response
        return response
