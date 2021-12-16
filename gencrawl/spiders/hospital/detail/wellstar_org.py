from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class WellStarOrg(HospitalDetailSpider):
    name = "hospital_detail_wellstar_org_us"

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items)

        urls_without_domain = response.xpath('//div[@class="contact-number"]'
                                             '/following-sibling::a[contains(text(),"Learn More")]/@href').getall()

        if not urls_without_domain:
            yield self.generate_item(items, HospitalDetailItem)

        else:
            for url_without_domain in urls_without_domain:
                url_without_domain_split = url_without_domain.split()
                url_without_domain_join = url_without_domain_split[0] + '%20' + url_without_domain_split[1]
                connector_url = 'https://www.wellstar.org/' + "".join(url_without_domain_join)
                yield self.make_request(connector_url, callback=self.parse_locations, meta={"items": items[0]},
                                        dont_filter=True)

    def parse_locations(self, response):
        items = response.meta["items"]
        item = deepcopy(items)

        item['address_raw'] = response.xpath('//div[contains(@class,"address")]//div/a').get()
        item['phone'] = response.xpath('//p[contains(@class,"Phone")]/a').get()
        item['fax'] = response.xpath('//p[contains(@class,"Fax")]/a').get()

        yield self.generate_item(item, HospitalDetailItem)