import scrapy
import json
import re


class QuotesSpider(scrapy.Spider):
    name = "digispider"

    def start_requests(self):
        urls = [
            "https://www.digikala.com/product/dkp-446827/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        information = re.findall("var variants =(.+?);\\n", response.body.decode('utf-8'))
        information = information[0]
        answer = json.loads(information)
        list_1 = []
        rates = []
        for i in answer:
            product = answer[i]
            price = product["price_list"]["selling_price"]
            lead_time = product["leadTime"]
            cancel_percentage = product["marketplace_seller"]["rating"]["cancel_percentage"]
            return_percentage = product["marketplace_seller"]["rating"]["return_percentage"]
            ship_on_time_percentage = product["marketplace_seller"]["rating"]["ship_on_time_percentage"]
            rate = (cancel_percentage + ship_on_time_percentage + return_percentage) / 3
            rates.append(rate)
            list_1.append((price, lead_time, rate))
        max_rate = max(rates)
        # print(max_rate)
        # print(list_1)
        # print(len(list_1))

        # تاخیر در ارسال به ازای هر 1 روز 4درصدد
        # به ازای 1 درصد پایین ازبالا ترین درصد,1درصد کاهش میابد
        for info in list_1:
            new_price = info[0] - (info[0] * (info[1] * 0.04))
            if info[2] < max_rate:
                new_price = new_price - (new_price * ((max_rate - (info[2])) * 0.01))
            if new_price != info[0]:
                print(f"{info[0]}------>{new_price}")
