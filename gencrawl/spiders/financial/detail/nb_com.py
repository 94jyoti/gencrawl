from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class NbComDetail(FinancialDetailSpider):
    name = 'financial_detail_nb_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        print(len(items))
        #file = open("nb.html", "w")
        #file.write(response.text)
        #file.close()
        #print(items[0]['temp_id'])
        #current_itemid=response.xpath("//a[contains(text(),'Skip')]/following::div[1]/@data-context-id").extract()[0].replace("{","").replace("}","")
        #share_classid_temp=items[0]['fund_url'].split("=")[-1]
        #print("current item id",current_itemid)
        #print("share calsss temo",share_classid_temp)
        #print(response.xpath('//a[@id="1252"]/@data-shareclass-itemid').extract())
        #share_class_id=response.xpath('//a[@id="'+str(share_classid_temp)+'"]/@data-shareclass-itemid').extract()
        #print("share class ifd",share_class_id)
        headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate, br","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Cache-Control": "max-age=0","Connection": "keep-alive","Cookie": "lang=en; www.nb.com=audience=2563a9a5-4a40-4559-8b67-866d83ef2285; SC_ANALYTICS_GLOBAL_COOKIE=16243c3d8c734f848da716c143088eed|True; AMCV_E9B80FC0539AE5990A490D45%40AdobeOrg=-1124106680%7CMCIDTS%7C18844%7CMCMID%7C09931076965856026570390653077113735069%7CMCAAMLH-1628742609%7C12%7CMCAAMB-1628742609%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1628145009s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; bm_mi=1617C66D091574135727A3EA01351A05~gG1haH47fdFAigo8KodG5wAd/9uMy3TuiADLFhoy+p0+fC7Zzvmv4aSI/QK0ISXMqT3hwznrJ+qZYxYN76JwWuWW0wttbSdZJJvggeKzbzgp7PyFow3nEsjPavmYeAS3VKRfpN6qfi2y01Cg90CE6xNN3yhOVjdFlTjUVt74epqykXPkzj2RtyL+hDvhC1MzoO4Lv1MJA2BwJ9yGbYockbMCVAvTPlL0A9WQtIG+HQcxN5qcMqP/OsGEDCMW8LZqZ5vulzt+Z/u2FBKcomwoRlxwmCe3tuIKmyAaTe3BaSlaFquMsQ9myDre2E9rjjOoy1aLyupqW3SZ4m9Gn9m/AXCvPQTJi+9DBGaP2gJbkD8=; ASP.NET_SessionId=htts11eymoyouunwbxn512yv; ak_bmsc=040FF29AF1C4EA1FFB4EABC5D2E36FA4~000000000000000000000000000000~YAAQVI0sMae9jJl6AQAAGXE+FQxBNipvtMeV33LnQlOlPToQLOFIgy/93pEUiGhkFZKHOF0iDlSBNRLTexHO+/y3jrZ1PjF0Hw6WRVZ6ugm253c5rHk88ag4nyufsrABZEAPJbamC3l9grjueT0WQVUMlZFDiGX7LmeS+9t1GQNVj5zT/ONOINlEGi5s+PrqOckGb4Tqlljua48TRnRDt1O9Cn/zVO1ZKuVIlMXQoOYJZ5vJ/Ugw/B0QlKeoHfw+MEfxfnblQpZZCkDkLInamZt5aUh1oEfzHEmk2g63uMDOMmuNdcBzth9Z8xXzVmQ8KA5zROGFK6B9GvUsj16LQ/MjFLL1/3Y2S8GoGFBy30B2t0hyr1IF4Z1/V3V8tE81gW6VoJyqdR1cPFXjM5bf6z1KIsIUb9I1ZkcrjbPzIk/5XmMqxIFUSozN8Kczt4hJ3kEAbOIXuYlue6d1Rgn8bdxmld/NJDqoh9wBxzegjBI8ED7F5apc1Niu1w==; DCID=0; Login=unknown; dslv_s=Less%20than%201%20day; s_cc=true; s_pvpg=Dividend%20Growth%20Fund; gpv_pn=Dividend%20Growth%20Fund; dslv=1628149042777; s_plt=5.88; s_pltp=Dividend%20Growth%20Fund; bm_sv=8D2BE6AB40D905E83A1ACAB96AEA62BD~cZfAnlnl5nBArj160LCemLUvQDHF6FLVyMNJMeIdg4IjHLgDzYuuJuWqWQozlPGZxOxE9nWGk4jMvF8VVZKuTWQ3Lz/3J7aab1oYabIRE86XIWHLl0KIVJDpAVYbWcMr33uWSw//0T4g78cD/FLmRQ==","Host": "www.nb.com","sec-ch-ua":' "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',"sec-ch-ua-mobile": "?0","Sec-Fetch-Dest": "document","Sec-Fetch-Mode": "navigate","Sec-Fetch-Site": "cross-site","Sec-Fetch-User": "?1","Upgrade-Insecure-Requests": "1","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
        #api_url="www.nb.com/api/Sitecore/Product/GetCharacteristics?nbmicode="+share_classid_temp+"&shareclassitemid="+share_class_id+"&currentitemid=%7B"+current_itemid+"%7D"
        #print(api_url)
        meta = response.meta
        meta['items'] = items
        headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate, br","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Connection": "keep-alive","Cookie": "lang=en; ASP.NET_SessionId=jadf0ztjhv5kouddlhyaxjtc; DCID=0; Login=unknown; AMCVS_E9B80FC0539AE5990A490D45%40AdobeOrg=1; s_cc=true; www.nb.com=audience=2563a9a5-4a40-4559-8b67-866d83ef2285; _sdsat_1_S_Audience=; SC_ANALYTICS_GLOBAL_COOKIE=16243c3d8c734f848da716c143088eed|True; AMCV_E9B80FC0539AE5990A490D45%40AdobeOrg=-1124106680%7CMCIDTS%7C18844%7CMCMID%7C09931076965856026570390653077113735069%7CMCAAMLH-1628742609%7C12%7CMCAAMB-1628742609%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1628145009s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.2.0; dslv_s=Less%20than%201%20day; s_pvpg=Absolute%20Return%20Multi-Manager%20Fund; gpv_pn=Absolute%20Return%20Multi-Manager%20Fund; bm_mi=1617C66D091574135727A3EA01351A05~gG1haH47fdFAigo8KodG5wAd/9uMy3TuiADLFhoy+p0+fC7Zzvmv4aSI/QK0ISXMqT3hwznrJ+qZYxYN76JwWuWW0wttbSdZJJvggeKzbzgp7PyFow3nEsjPavmYeAS3VKRfpN6qfi2y01Cg90CE6xNN3yhOVjdFlTjUVt74epqykXPkzj2RtyL+hDvhC1MzoO4Lv1MJA2BwJ9yGbYockbMCVAvTPlL0A9WQtIG+HQcxN5qcMqP/OsGEDCMW8LZqZ5vulzt+Z/u2FBKcomwoRlxwmCe3tuIKmyAaTe3BaSlaFquMsQ9myDre2E9rjjOoy1aLyupqW3SZ4m9Gn9m/AXCvPQTJi+9DBGaP2gJbkD8=; ak_bmsc=040FF29AF1C4EA1FFB4EABC5D2E36FA4~000000000000000000000000000000~YAAQVI0sMR+2jJl6AQAAOm0EFQxp193t7YJPhN2HMwxB0z/sc/RItwS6ooyuMHgW1csYh3V2tOz+4t7jTlelR2LlTpXD7YBoD/5f2gOAvGnINjvokayuNPxVUNhDYkURLOV4Et5QgYnW6fZRgHetPdsCnRv4EpvKAhONPzj2TtOs+dDC4pZgUY3prJdf96nWQhbcxJ1nvJ80phFpF8zVY1U3tIJ4TP9LuhtmQpjsaVVmwjqSmmNYzdgn7vjVv8tqgrwTlokRV1r5uTQ77Isomt/Dnz8VfWws1r9Ba5D3GMoM3psftA/nUJixnjZg7KAD6NvYMPVhnVu/SqqIVdEUeVFi+s1To4PoYj3Ea2Xj5UZF52rNnVp7eSTTnK/8F0yuqgEmIZYHVduCB98f9XihMJ9pFLkdYtWyyR9HSD5W0FhQku9Ons361imEwzHSreLqQ3sLKEU0qz0hxkivclNWqt0dkj9aoxFNYGc=; s_sq=%5B%5BB%5D%5D; dslv=1628146158774; nb#lang=en; s_plt=4.98; s_pltp=Absolute%20Return%20Multi-Manager%20Fund; bm_sv=8D2BE6AB40D905E83A1ACAB96AEA62BD~cZfAnlnl5nBArj160LCemLUvQDHF6FLVyMNJMeIdg4IjHLgDzYuuJuWqWQozlPGZxOxE9nWGk4jMvF8VVZKuTWQ3Lz/3J7aab1oYabIRE87h1RiPAb68962fcWSbNNpwNSAO2gnC5gWJGa35hPYD8Q==","Host": "www.nb.com","sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
        #url =items[0]['fund_url']+"#2AD3B41F89254DDA891640F50F8A20D2"
        url="https://www.nb.com/en/us/products/mutual-funds/absolute-return-multi-manager-fund?nbmi=1252"
        #print(url)
        yield self.make_request(url, callback=self.dividends,meta=meta,method=Statics.CRAWL_METHOD_SELENIUM,headers=headers,dont_filter=True)
    def dividends(self,response):
    	print("yahan hun")
    	items = response.meta['items']
    	file=open("nbbbbb_dnckd.html","w")
    	file.write(response.text)
    	file.close()
    	#print(response.xpath("//div[contains(text(),'CUSIP')]/following-sibling::div/text()").extract())