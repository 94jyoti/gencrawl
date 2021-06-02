from scrapy.downloadermiddlewares.retry import RetryMiddleware


class CustomRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        print("I am hereeeeeeeeeeeeeeeeeeeeeee")
        if spider.retry_condition:
            print(spider.retry_condition)
        if response.status in [503]:
            if 'https://carmanuals2.com/sc/' in url:
                url = url.replace('/sc/', '/d/')
                request = request.replace(url=url)
            reason = 'blocked with 503 response staturls'
            return self._retry(request, reason, spider) or response
        return response

    def process_request(self, request, spider):
        print("I am hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        #return request

    def process_exception(self, request, exception, spider):
        print("Xxxxxxxxxxxxxxxx")
        print(exception)
        return None