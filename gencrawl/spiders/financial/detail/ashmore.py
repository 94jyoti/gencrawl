from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class AshmomDetail(FinancialDetailSpider):
    name = 'financial_detailhmore_com'
    custom_settings = {
        "HTTPCACHE_ENABLED": False,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "CRAWLERA_ENABLED":True
    }

    def start_requests(self):
        for i, obj in enumerate(self.input):
            print(i)
            url = obj[self.url_key]
            #print(obj[self.pagination])
            pagination_fields =obj
            print("-----------------------",pagination_fields) 
            obj['selector'] = Statics.SELECTOR_ROOT
            print(obj)
            static_url = "http://www.ashmoregroup.com/multilingual-self-cert"
            headers = {"Connection": "keep-alive", "Accept": "*/*", "X-Requested-With": "XMLHttpRequest",
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
                       "Origin": "http://www.ashmoregroup.com",
                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       "Referer": "http://www.ashmoregroup.com/?sc=", "Accept-Language": "en-US,en;q=0.9",
                       "Accept-Encoding": "gzip, deflate", "Host": "www.ashmoregroup.com","X-Crawlera-Session":"create","X-Crawlera-Cookies": "disable"}
            yield scrapy.Request(static_url, headers=headers, method="POST",meta={'fund_url': url, 'cookiejar': i}, callback=self.make_request,dont_filter=True,body="market_country=usa&language=en-us%2Cen-us-ii%2Cen-us-ipi%2Cen-us-ifa&role=individual+investors&form_build_id=form-T0930Y0jj-2BK9pSGCoHmYL1hSdEnq_rbuGiHfAjNcI&form_id=taxonomyuserroles_multilingualselfcert")

    
    
    def make_request(self, response):
            print("111111111111111111")
            #items = self.prepare_items(response, default_item)
            
            file = open("t.html", "w")
            file.write(response.text)
            file.close()
            fund_url = "http://www.ashmoregroup.com/multilingual-self-cert/2?sc="
            print(fund_url)
            print("rererrststysusuu",response.headers)
            headers = {"Connection": "keep-alive", "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1",
                       "Origin": "http://www.ashmoregroup.com", "Content-Type": "application/x-www-form-urlencoded",
                       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                       "Referer": "http://www.ashmoregroup.com/?sc=", "Accept-Language": "en-US,en;q=0.9","Accept-Encoding":"gzip, deflate","X-Crawlera-Session":response.headers["X-Crawlera-Session"],"X-Crawlera-Cookies": "disable"}
            yield scrapy.Request(fund_url, headers=headers, callback=self.make_final_request, meta={'cookiejar': response.meta['cookiejar']}, method="POST", dont_filter=True,body="agree_terms=1&op=AGREED&form_build_id=form-7umQrrioxwQxDSEl1PQ5XqVnL9PS8AgI1eGKdiQJdz8&form_id=taxonomyuserroles_multilingualselfcert_terms")

    def make_final_request(self, response):
            print("22222222222222")
            items = self.prepare_items(response)
            print("222",items)
            file = open("testtttttt.html", "w")
            file.write(response.text)
            file.close()
            print("headrsrssrsrsrsrsrsrsrs",response.headers)
            fund_url = "http://www.ashmoregroup.com/us-ii/our-funds/40act-aemlcbf-c-inc-usd"
            print(fund_url)
            print(response.meta['cookiejar'])    
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", "Connection": "keep-alive", "Host": "www.ashmoregroup.com",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36","Referer":"http://www.ashmoregroup.com/us-ii/our-funds","X-Crawlera-Session":response.headers["X-Crawlera-Session"],"X-Crawlera-Cookies": "disable"}
            yield scrapy.Request(fund_url, headers=headers, callback=self.parse_mainurl, meta={'cookiejar': response.meta['cookiejar']}, method="GET", dont_filter=True)

    def parse_mainurl(self, response):
            items = self.prepare_items(response)
            print(items)
            print("33333333333333333")
            file = open("testtttttt111111111111.html", "w")
            file.write(response.text)
            file.close()
    '''
            yield items[0]
            print("aleeneknk")
            if(response.meta.get('dont_follow')):
            	return 
            pagination=response.xpath("//select[@name='shareclass']//option[not(@selected)]//@value").extract()
            for i in pagination:
            	url="http://www.ashmoregroup.com"+i
            	yield scrapy.Request(url, headers=headers, callback=self.parse_mainurl, meta={'cookiejar': response.meta['cookiejar'],"dont_follow":True}, method="POST", dont_filter=True,body="agree_terms=1&op=AGREED&form_build_id=form-7umQrrioxwQxDSEl1PQ5XqVnL9PS8AgI1eGKdiQJdz8&form_id=taxonomyuserroles_multilingualselfcert_terms")
        	print(pagination)
        	
            print("share
             classssss",response.xpath('//select[@name="shareclass"]//option[(@selected)]//text()').extract()[0])
    '''