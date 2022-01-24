import json
from scrapy.http import HtmlResponse
from gencrawl.util.statics import Statics


# people checker middleware
class PCMiddleware():

    def process_request(self, request, spider):
        meta = request.meta
        cached_link = request.meta.get("_cached_link")
        # if no cached api url, disable this middleware for that request
        if not cached_link:
            return None

        if request.meta.get('dont_pc_cache'):
            return

        if request.meta.get("retry_times") and request.meta['retry_times'] > 0:
            _retry_url = request.meta.get("_retry_url")
            if _retry_url:
                meta['dont_pc_cache'] = True
                return request.replace(url=_retry_url, method='GET', meta=meta)
            else:
                return

        meta['dont_proxy'] = True
        # don't use selenium middleware for cache url
        meta['dont_selenium'] = True
        # to avoid repeated request loop
        meta['dont_pc_cache'] = True
        meta['_pc_original_url'] = request.url
        meta['_retry_url'] = request.url
        request = request.replace(url=cached_link, method='GET', meta=meta)
        return request

    def check_uc_reponse_valid(self, body):
        if '<h1>Resource Limit Is Reached</h1>' in body:
            return False
        elif '<h1>504</h1>' in body:
            return False
        elif '<title>Error</title>' in body:
            return False
        return True

    def process_response(self, request, response, spider):
        original_url = request.meta.get('_pc_original_url')
        if not original_url:
            return response
        del request.meta['dont_pc_cache']
        del request.meta['dont_proxy']
        del request.meta['_pc_original_url']
        del request.meta['dont_selenium']

        request = request.replace(url=original_url)
        try:
            body = response.json().get("all_body", {}).get("page_source")
            if self.check_uc_reponse_valid(body):
                status = Statics.RESPONSE_CODE_OK
            else:
                status = Statics.RESPONSE_CODE_PC_INVALID
            body = str.encode(body)
        except:
            body = Statics.MESSAGE_PC_FAIL
            status = Statics.RESPONSE_CODE_PC_FAIL
        return HtmlResponse(
            original_url,
            status=status,
            body=body,
            encoding=Statics.ENCODING_DEFAULT,
            request=request,
        )
