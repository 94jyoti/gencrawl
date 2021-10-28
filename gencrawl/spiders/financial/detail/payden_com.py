from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider

from datetime import datetime
import datetime
import urllib.parse
import re
from gencrawl.util.statics import Statics
# import urllib
import itertools
import logging
import requests
from lxml import html
from scrapy.selector import Selector
import copy


class PaydenDetail(FinancialDetailSpider):
    logging.basicConfig(filename="hsbc.log", level=logging.INFO)
    logging.info("InvestorFundsUSHSBCDetail")
    name = 'financial_detail_payden_com'

    
    def get_items_or_req(self, response, default_item={}):
        logging.info("InvestorFundsUSHSBCDetail...get_items_or_req")
        items = super().get_items_or_req(response, default_item)
        #print("Items:",len(items))
        meta = response.meta
        meta['items'] = items

        final_items = []


        selector = scrapy.Selector(text=response.text, type="html")
        tickers = selector.xpath("//select[@id='drpClass']/option/@value").getall()
        if len(tickers)>1:
            #yield self.generate_item(items[0], FinancialDetailItem)
            for ticker in tickers[:]:

                meta['final_items'] = final_items
                
                meta['ticker'] = ticker
                form = {
                        "__VIEWSTATE":selector.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                        "__VIEWSTATEGENERATOR":selector.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                        "__EVENTVALIDATION": selector.xpath("//input[@id='__EVENTVALIDATION']/@value").get(),
                        "drpClass":ticker
                        }
                h = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
                }
                yield scrapy.Request(response.url,method='POST',body = urllib.parse.urlencode(form),headers=h,callback=self.distributions,dont_filter=True,meta=meta)
                
        else:
            for i in items:
                meta['final_items'] = final_items
                meta['item']=i
                url = 'https://www.payden.com/capitalGains.aspx'
                yield scrapy.Request(url,callback=self.get_capital_gains_info,dont_filter=True,meta=meta)

                #yield self.generate_item(i, FinancialDetailItem)
    def distributions(self,response):
        meta = response.meta
        ticker = meta['ticker']
        final_items = meta['final_items']
        selector = scrapy.Selector(text=response.text, type="html")
        cusip = selector.xpath("//td[contains(text(),'CUSIP')]/following-sibling::td/text()").get()
        share_class = selector.xpath("//select[contains(@name,'Class')]/option[@selected]/text()").get()
        portfolio_assets = selector.xpath("//td[contains(text(),'Fund Total Net Assets')]/following-sibling::td/text()").get()
        maximum_sales_charge_full_load = selector.xpath("//td[contains(text(),'Sales Charge')]/following-sibling::td/text()").get()
        share_inception_date = selector.xpath("(//td[contains(text(),'Share Class Inception Date')]/following-sibling::td)[1]/text()").get()
        item = meta['items']
        item_copy = copy.deepcopy(item)
        item_copy[0]['nasdaq_ticker']=ticker
        item_copy[0]['cusip']=cusip
        item_copy[0]['share_class']=share_class
        item_copy[0]['portfolio_assets']=portfolio_assets
        item_copy[0]['share_inception_date']=share_inception_date

        final_items.append(item_copy[0])

        #print("dddd:",final_items)

        meta['item']=item_copy[0]

        url = 'https://www.payden.com/capitalGains.aspx'
        yield scrapy.Request(url,callback=self.get_capital_gains_info,dont_filter=True,meta=meta)

    def get_capital_gains_info(self,response):
        meta=response.meta
        item = meta['item']
        
        years_list = response.xpath("//select[@name='ddlYear']/option/text()").getall()
        print(years_list)

        #final_items.append(item)
        meta['nasdaq_ticker'] = item['nasdaq_ticker']

        #open(item['nasdaq_ticker']+'.html','w',encoding='utf-8').write(response.text)

        capital_gains_data = []
        meta['capital_gains_data'] = capital_gains_data
        for year in years_list:
            print(year)
            #print("Viewstate:",response.xpath("//input[@id='__VIEWSTATE']/@value").get())
            meta['year'] = year

            url = "https://www.payden.com/capitalGains.aspx"

            form = {
                        "__VIEWSTATE":response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                        "__VIEWSTATEGENERATOR":response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                        "__EVENTVALIDATION": response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
                        
                        

                        }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
                }

            body = urllib.parse.urlencode(form)+"&ddlYear="+year.replace(' ','+')+"&ImageButton.x=10&ImageButton.y=20"
            #print("body:",body)
            yield scrapy.Request(url,method='POST',body = body,headers=headers,callback=self.get_capital_gains_info_2,dont_filter=True,meta=meta)
                
    def get_capital_gains_info_2(self,response):
        meta = response.meta
        nasdaq_ticker = meta['nasdaq_ticker']
        year = meta['year']
        item = meta['item']

        final_data = []
        data = []
        capital_gains_data = meta['capital_gains_data']
        #open(nasdaq_ticker+str(year)+'.html','w',encoding='utf-8').write(response.text)

        #print("hello")
        #print("dd:",response.xpath("//tr/td//text()").getall())
        for tr_block in response.xpath("//tr"):

            #print("here")
            #print("tr_block:",tr_block)
            reinvest_NAV = tr_block.xpath("td[2]/text()").get()
            short_term_per_share = tr_block.xpath("td[3]/text()").get()
            long_term_per_share = tr_block.xpath("td[4]/text()").get()
            cg_record_date = tr_block.xpath("td[5]/text()").get()
            cg_ex_date = tr_block.xpath("td[6]/text()").get()
            cg_pay_date = tr_block.xpath("td[7]/text()").get()
            ticker = tr_block.xpath("td[8]/text()").get()
            data.append([reinvest_NAV,short_term_per_share,long_term_per_share,cg_record_date,cg_ex_date,cg_pay_date,ticker])
            #print("data:",data)
       
        #print("data:",data)
       
        capital_gains_data.append(data)

        if len(capital_gains_data)==17:

            #print("sss:",capital_gains_data,len(capital_gains_data))

            url = "https://www.payden.com/dividends.aspx"

            yield scrapy.Request(url,callback=self.get_dividends_info,dont_filter=True,meta=meta)

    def get_dividends_info(self,response):

        meta = response.meta
        item = meta['item']

        months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        months_label = ['January','February','March','April','May','June','July','August','September','October','November','December']
        years_list = response.xpath("//select[@name='ddlYear']/option/text()").getall()
        print(years_list)


        
        #meta['months_label'] = months_label

        dividends_data = []
        meta['dividends_data'] = dividends_data

        #months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        #months_label = ['January','February','March','April','May','June','July','August','September','October','November','December']
        
        #years_list = ['2021']

        meta['years_list'] = years_list
        meta['months'] = months

        

        for year in years_list:
            for c,month in enumerate(months):
                print(year,month)
                #print("uuuu:",response.xpath("//input[@id='__VIEWSTATE']/@value").get())
                meta['year'] = year
                meta['month_label'] = months_label[c]

                url = "https://www.payden.com/dividends.aspx"
                
                form = {
                            "__VIEWSTATE":response.xpath("//input[@id='__VIEWSTATE']/@value").get(),
                            "__VIEWSTATEGENERATOR":response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),
                            "__EVENTVALIDATION": response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
                            
                            

                            }
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
                    }

                body = urllib.parse.urlencode(form)+"&ddlmonth="+month+"&ddlYear="+year+"&imgButton.x=28&imgButton.y=10"
                #print("body:",body)
                #body = '__VIEWSTATE=oBrmVNvYcmljAU99ZuuAEKaBdAsHmE5x22nMPtyVnyp7V2i436nMajp4moVReMlqOSGbEbNecPYxP5PHgHb7U7r%2BAhPESm88xWUwR9rqXIvEPqsvzgjGaGeklnFgCvMt8TjDxDkP7YwGkaS1LdH4x8%2BNrxRDSY8xakScjVsRP%2B1K5BIPwyieRHivPPzG7Hijc8miB5eDvRxdiTn8OPG9CzieTxSVLzDZwq%2FXfQBvvo1CXTda%2FlPlI%2BTnvNfy0VARLkvq4YLgNCGQtx5ixSS0sBbor4Nop%2BTfpEY4DJbUzNQP3UwFktTA7kr9AgROZeuIZq4HDbwrPprVs3tJXIbOpUtc9N%2BhdgG0z%2B6XkA%2BZ5QA159C3ZZgj7Y%2FYrKrBZGk2rhRXfClHBen09K%2Bl5xBo28KBlnq41Kmy9befaYWiCunpWFWyZAOMJH2%2BXEvcF2XIn0gOH1T1vpESKgPr3QjMsBGp1asDM7EFunQ4sLU1WfZVRMUNmQpbY%2FgSci5UeHfpigezgHe7XPFK1F%2Blzm77mjRZPzrtSYSI03uz2wDquSXW%2Ba0RGqsqPl1wpZS8h%2BnT6Q6KR5dHQhfQ9enpxr91HhBU0v7s7ypVSJkDmXJwS6QsJshs3G1xG5h0QkRD4Dcyj70NKSRxrlS1BogWsD5SRHVFtgWUPpnnKhLRebPLJhS1uwtBgw0WZUXsBQsvuuMVgQ74fAwdMlUPurHo9OrFipp%2Btg0nwRmMOzlnpLH%2FR01AnySpdvo7Z71M9poD5AtlQ4f08J8tzP7UMEjzMufTbyNulAx5peQaKbsn4CuPtviyO7%2BI%2FTaA0MXz0OtINWUYFEx3whD09fypteo5B1t07spYgLwNsN1QDGkNa6yh61Da1ocDmCDjsMTz90ZrqOzve8oNSTB90TQtO0ooB8zqTrbtseO62C8Co2TmSOrmr5vnb1%2BI2RjumCwilC8bjaePir6Y2iRuhApvfiKBOk38g%2FSVq8bS8AbV0Bn82Uj%2B13Iv8kMuPCbatTQX3fjGytUmFq41e3RMojMWIgjE19o3xGR4AcQxdo%2FauDhGwZKfZcwkCkChjRsCx6Hd%2FypSKNXFZnwzBQ4hmeAUmc8gYd%2BnXlJQml2QLgSTD5A10aTQfrpaq0665d8IDZJEC8jJSCO1cVZ14gnZge8NsgfTA5aufMywBnvNTeF%2FOSnSr%2FeJFVwORSFhayoDddyWH%2BI9Cc0tTu31%2FSRNSNML1biFWILc83P0JpKKyFSpf7PGLXp9ljhTmTyf%2BWl40kOOiowoCjta9SiZwnIo1meNor4WAIrg9yNpCSjJGZwwS0mB3mWq8RvEONL7yEV91fL5cfRNDpfYSD5q2IdfKMB9b5qnjK3aE1Ovt10cUw3BwNTkK9j%2BoeGeVaXvzvdih7zh6PtvHmpAgeONnC0RegC%2FXgZdg3OzRkbt3jaeUjmadBy5p2qkH%2BBl6EMtv8NF59reCtAzFIOi88m8bge8NqB1OgPYnrrIbGdIxZ1pPPnChT550Vc3BbVZAtM0LH5qACqLoAnunE%2BEEi%2B%2B9SJpu7ESkoBi68CNwYS72Zd%2Bbok7X1AW9Ncnl8H4ueZMVpvos5fKD7idDGJ6XEGvEXgDGUt3ezMIrkwCmyG4bTHXOOxA3W5s6MOkmO03aB%2FDZvbtaz6PGCOyfOAb5M5h%2BnGBB1DHlXVBgoG4mdBF1XjxAkcV8a8ta3X1L%2BjnM6%2BcufkPuZqQ6zZ%2BCB%2BSm2bsBUorPW7TMdp3Yhj1WiV68UHrCkT9HZkYVtdFMuhyLWE6c7wYB3%2BPLvNGHdWGRPgmci4hZ%2Bdm%2BF%2F7I65OcvErbma1dKzPjrD5NNgfWB5w2eTCO82ikJTRQfQYlB3%2BkZzH5yUvRx4CtEZW%2FzAypdkUlDr%2FQlVC9H%2F5ylGzTZxaUR0%2B%2BCm32z7VV5wkbaZaZ0x2KTft2jxSrlXd6x%2ByBPOzGESURAddgqbOfi62GVURfMlEakYemylnzTg8vxxS9dQMbKIC6cUKHDhdfCVydQky82PKW04ZcBgo4zSYeK%2Fv7xyiwAg7FfDNgoPgfQU4QJmfTiV7wjC83EEt3aQD6Uv03A9Np5jMFfai%2B86aRnv0l9JwyB5%2B9wjpeRpbQazoI4%2F1Np%2F0OYFcZML5jayBt2p43UteLa2jyOPRttkjlqc68Wee9TNcvqKcJFnPFJrl4aKtjrfRyawt9TZPdGFkE35R3aSyVJ6VtTsdBmrf9YDdl%2Bz7ZytUPG6RwU%2B%2FzaeTpz8ReE11OXbM%2FEUrFhK909ZaLx6uujhP1MzFuN5ONeWe3PaalohgBCN8A0gVfq5A0j2FRY1%2FK4JZtd3y3uTHUmFKXTBkWOW1Yz3BCidPfHOC2%2FID6rnvhyiSKC%2FnsVhrKfH23L3HZSQ4N%2FjedbTJNbhLxRUcmf%2Bdk0yVKA7C2%2BhRnY7cdj07Vbv%2BcW47o4ldDkrj9%2FWFNAFdsMsoxuRGGzUJrbLKPiL92knvLp2aMzy%2FifCgL%2F5yV9mFdL7rH06YU2%2FcuGCLss1%2F6c2nZHKfvSf8o1cZP5TaZOaPmE6HphjAXvrUHf2D8F6aqCgfKYZbiv8BOdLQ%2FFQKqQz2ynyabKtVp3oY0IuxVM6Gwmlpxlx%2BRM6tqxxteRjsRW9js9uznia4ldMUNUsfA6QSkU2KJFbMhBJFve%2FcLx5y5wWhIeoMFibknodnu9YRd%2FFafSrRSivH4JM6U5wERARjxY9dBm%2FoQMByEJFjXOuwvZRTAx73v0zBgk54fGXR0Zs4jy%2F%2BGb%2BWcpNq4a66VVHbNy3tIDVqNDwRniEvkUt%2FN0vLET5d%2BaGOEptoplRDmFB3BUnbMZutuihjnMjcC%2B%2B6AIY7qsqqAjzLm%2Fa59YLYvxovtHv1EdMy%2BJaAC6qWouGknVsAPWx6hetIcI9Fm6fGVhc7nMDS6SFTOjKyhOK%2F3dJCnuRjxLtIHgnun6mZH9YNeEsI%2BxASG4X%2By8Cbnyq2t2RivparHjEcLdy0bXfGJxQyKbazr%2BDhAK2VhnoMClOcTlrWayipXRJfug7%2F0jSeMY5QkLGAuzFea3L4tC9bpVHCSHf%2Fuf%2BQsVc77npmX2GjRdVszF5Z27abM57cwc50PJCn7%2BdUB%2FxYZx9amvXv%2FdrH318YYCkaMgx1GOTWLtQ24crJ4Xqy%2F4UflQDTpdl9Ya3NVBDLyNxU6qceBVleduZZGyyN%2BcUN7g%2BMUWAMle1eqYlfl%2BjnJYcKm1e411QYXQTDMaIAxSsnZ%2FXHLq39E4EejC%2F4Ra9pCkoDiRC1WpMpQUo9awUZAld6Fmv%2B7iCUckHfuCFckXs6ntow8iYg9tjYHtfd5BKe1%2FrECPgiTSuRpn8660XWFpmE4skC7Srwd4LjFQg3jbmr5arVlaZMQ6be%2FzLi1RzRK9HCGYhpCld89iiYUB9Clh9kpJRuRke%2B%2BI%2B91lN6vlnWgMXj6fmtwu8FH3eSmpc0bwKQdTG0T6JxJQ7jIhpbniD51pa3PJ9q8kJyD2dOb7HOTjXmi6rJe%2Bmgsijzb8OPGlVCiytBpOubBDilmeLFEtG5yBShfjEpuOZ2UoByfVj7sJCL4wssxtCxSpVFVy%2F1Wh1sssWXBIj6PMUFnmWI4%2BfRPExBeT1n4bHYKebYZZln%2BsE4wMdxpA03uzGfMsY37%2BLCzaEQZqef94DipHctNJQmGFFNlNMCoZ%2FNiZW7aabrR2nXma%2BwZX%2BhOpxosjUGOhDWsWXMZV4ehirt6nE5NZt11dENVrxt2EeU1yDoE4SFJcZznZYP2dWYYMk2k%2FGdFOflmcmPOScZO%2BML0ya1q3caZhobOoPS3kuvnom%2FyGgUk7wcHIe6D9XheBj1GSS8oxD4QO6CkbDDgU%2BGB7Q9mcRCRnWFhkPiqnCYfSurCPcOmja%2FRr4A3%2BPE7agGOo4%2Fba76%2BWvoD48tmammfbwHOLZ5SZ1zjzaQXXwBpXv4qsMuZbcJB6Yhvyaxc55DZ%2BsTbCZs%2FjbEwRSRETNG1N9llWrDSe1dKT0c%2FaqIVsc7kwEiVygiuNSWIVU7XWVOG%2FQXwYjkTIGeKX%2FInIkAeoNtAHANLjAMjS4EFCuLevrkTPMpdEGvbwDBraNdpFRQ7o3Cxu8w4m2zgrr6C4vheUI2SRa847B3PgvPLdkSJzqR67b1iJ2AGYymI0P%2BMP7V%2FClv9b669g4Le%2BLPwwH3ijvFzwgAJ9lQJIZxj5IcUMFj3hvFh0fpKG9gS%2FXSsOVZKdACBy4kyL0aQesHSXsCEOBK2NjC8uIlz73Ubm6SqRWU2x%2BUmJ5eJiU%2F%2BPZ9GSIDhq%2FdoA%2BIqLNHSDP%2FAD1oyG4RK4L%2Fiu2sqRv0eVrYFDc%2FRXsTGWF3xoTS0%2FnNcH3jzwmQ41zzYDplyRYQZdY3WquNz30eemRllGsmNX5BDcOjClFe23eNl5QXkvSSSpedSMkTy%2F3iQUr5bj%2BrqY9be%2FvGHB9v7lzmnCUHSf8WND226Ze5H0c3f3Y2TSr9Pb%2BBLfLL%2BgQr1pvcVF8dWR7Viq7ZOQKTpsF1%2Fk3mi%2F7jpmknSBZ%2FB4%2B4eg7NPq3LIVreKn%2BofFN8RpTzonCrUDU0guYXqDQtj%2FKjK524IcpBCUJLJEhkTtqtl4moyaBDjflPMyECDx02P9DX%2B2l6FX%2BM8A55P4zuxecmrV%2F1DZTJtInBwNgQ3y4R9%2BU0HYiptkvoJIY2rP3d3tH%2FxUpvkWshMSXs1CMryg2txvGfTQN4O1lQeFCk7%2BO9XW5VUhL%2FbR%2BeuKiHhhImY896%2BfhnFdGjXMASXxhfXZovJTbZDkTfPj8tWzhGTPVZwYVfMxohA9LY8y75aAalvmov1%2F6P8mNuM9WKCZHP2WO%2FrKm6Z7p%2BCe0KskRGC2a8LRdBtZGSDZN7qsTra0GiCHdySd7xePqK154QIbUoyvz7mS%2BWWXFVAQ%3D%3D&__VIEWSTATEGENERATOR=882C0A18&__EVENTVALIDATION=F9LCyKMwmrcJhjBoNyiZuBqn7OankZzCYXrAKPUtv8w6cEX2Yhm7tHRoPmbzN3h6nzXduVEcE2JLid5lPaqqq3ifbfCAWd%2BVtcHEctZ6JWA63LHcT7Nr4YuzIu8XTuucQB45nTw%2BbROq1OG6ho0%2FpkfRCsmprikdWBgvIfd1tK1m1MIL%2FTIM5Hi025Mb2VfQBODu73I9B3TeTcslTqCrCk5Aa23S%2BA%2FCSDH0dEzpMySWBHe%2FKEX8pr4lSYlUlzJwjHxoL4kXPKqTonYYqiuU654uCib2e%2FSLKGN3hAse48waqEvewuvrmtBXWFt3d07h1SVXakEYatCEUU8xyS%2FNVoCD3wJsgYxnZg7mSZax7s3V%2F%2FK4YmHW0rGzo3MB22i0A2JqXXlFzFKb%2BTIoL0UGQy%2F3lclMMYjqku5t10lwwPrllYZF0Zmo0v7cz8jvHyH3A3szy2j05hCQHL3BZywwpwPEXFA7qF5sGgz%2FYVh2nlH2ibjVrHV6smK8maUvBumoCpQqtzfRePPbFNSw8f0WWofRu1U4KV725qeL1xpSHO5umXEkDwf12eyTpjz1qh0IB7sw5rzb%2BD%2By5JdAyX5Jj6RygD4tvsM8DtOKPfto5S4rkS%2FCQG2OMlrQiedOlfuOGDEC5tiOERhaO14oTQjalR9GH4TPL5b5zZYVjX1q%2BOBlC0%2BaJtqsh2sxeHiLdQUw&ddlmonth=01&ddlYear=2021&imgButton.x=33&imgButton.y=16'
                yield scrapy.Request(url,method='POST',body = body,headers=headers,callback=self.get_dividends_info_2,dont_filter=True,meta=meta)
                
    def get_dividends_info_2(self,response):
        meta = response.meta

        item = meta['item']
        years_list = meta['years_list']
        months = meta['months']
        month_label = meta['month_label']
        year = meta['year']

        #open(month_label+year+'.html','w',encoding='utf-8').write(response.text)

        dividends_data = meta['dividends_data']
        capital_gains_data = meta['capital_gains_data']
        nasdaq_ticker = meta['nasdaq_ticker']

        capital_gain_list = []
        dividends = []
        data = []
        for tr_block in response.xpath("//tr"):

            dividend_reinvest_NAV = tr_block.xpath("td[2]/text()").get()
            dividend = tr_block.xpath("td[3]/text()").get()
            ticker = tr_block.xpath("td[4]/text()").get()
            data.append([dividend_reinvest_NAV,dividend,ticker,month_label+" "+year])
            #print("data:",data)
        dividends_data.append(data)

        print("aaa:",len(dividends_data),(len(years_list)*12),nasdaq_ticker)
        if len(dividends_data)==(len(years_list)*len(months)):
            #print("bb:",capital_gains_data)
            print("cc:",dividends_data)

            for data1 in capital_gains_data:
                for data in data1:
                    #print("ee:",data[6],nasdaq_ticker)
                    if data[6]==nasdaq_ticker:
                        cg_ex_date = data[4]
                        cg_record_date = data[3]
                        cg_pay_date = data[5]
                        short_term_per_share = data[1]
                        long_term_per_share = data[2]
                        cg_reinvestment_price = data[0]
                        data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": "", "cg_reinvestment_price": cg_reinvestment_price}
                        capital_gain_list.append(data_dict1)
            
            for data1 in dividends_data:
                for data in data1:
                    #print("ff:",data[2],nasdaq_ticker)
                    if data[2]==nasdaq_ticker:
                        per_share = data[1]
                        dividend_reinvest_NAV = data[0]
                        ex_date = data[3]
                        pay_date = data[3]
                        record_date = data[3]
                        data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": dividend_reinvest_NAV}
                        dividends.append(data_dict2)          

            item['capital_gains'] = capital_gain_list
            item['dividends'] = dividends


            yield self.generate_item(item, FinancialDetailItem)





    