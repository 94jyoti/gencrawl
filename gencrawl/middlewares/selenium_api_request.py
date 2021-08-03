import json
from scrapy.http import HtmlResponse
from gencrawl.settings import SELENIUM_URL
from gencrawl.middlewares.selenium_request import GenSeleniumRequest

class GenSeleniumApiMiddleware():
	def process_request(self, request, spider):
		if not isinstance(request, GenSeleniumRequest):
			return None
		if request.meta.get('dont_selenium'):
			return 
		data = {
				"xurl":request.url,
				"xxpath": "",
				"xcon":"",
				"load_method":"selenium"
				}
		headers = {
				'Content-Type':'Application/Json'
			}
		meta = request.meta
		meta['dont_proxy'] = True
		meta['dont_selenium'] = True
		meta['selenium_original_url'] = request.url
		request = request.replace(url=SELENIUM_URL,method='POST',headers=headers,body=json.dumps(data),meta=meta,dont_filter=True)
		return request

	def process_response(self,request,response,spider):
		if not isinstance(request, GenSeleniumRequest):
			return response
		originalUrl = request.meta['selenium_original_url']
		del request.meta['dont_selenium']
		del request.meta['dont_proxy']
		del request.meta['selenium_original_url']

		request = request.replace(url=originalUrl)
		
		return HtmlResponse(
			originalUrl,
			body = str.encode(response.json()['html']),
			encoding = 'utf-8',
			request = request,
		)
		