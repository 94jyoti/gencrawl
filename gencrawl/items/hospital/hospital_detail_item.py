from gencrawl.items import BaseItem
from scrapy import Field


class HospitalDetailItem(BaseItem):
    raw_full_name = Field()
    first_name = Field()
    middle_name = Field()
    last_name = Field()
    suffix = Field()
    designation = Field()
    search_url = Field()
    doctor_url = Field()
    speciality = Field()
    affiliation = Field()
    practice_name = Field()
    address = Field()
    address_line_1 = Field()
    address_line_2 = Field()
    address_line_3 = Field()
    city = Field()
    state = Field()
    zip = Field()
    phone = Field()
    email = Field()


