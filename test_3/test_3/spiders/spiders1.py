import scrapy
import json
import re


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            "https://www.digikala.com/product/dkp-446827/%D8%B4%D8%A7%D9%85%D9%BE%D9%88-%D9%BE%D8%B3-%D8%A7%D8%B2-%DA%A9%D8%A7%D8%B4%D8%AA-%D9%85%D9%88-%DA%98%D8%A7%DA%A9-%D8%A2%D9%86%D8%AF%D8%B1%D9%84-%D9%BE%D8%A7%D8%B1%DB%8C%D8%B3-%D9%85%D8%AF%D9%84-act-implant-%D8%AD%D8%AC%D9%85-150-%D9%85%DB%8C%D9%84%DB%8C-%D9%84%DB%8C%D8%AA%D8%B1",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        answ = re.findall("var variants =(.+?);\\n", response.body.decode('utf-8'))
        answ = answ[0]
        answ_1 = json.loads(answ)
        list_1 = []
        rates= []
        for i in answ_1:
            product = answ_1[i]
            price = product["price_list"]["selling_price"]
            lead_time = product["leadTime"]
            on_time = product["marketplace_seller"]["rating"]["ship_on_time_percentage"]
            return_percentage = product["marketplace_seller"]["rating"]["return_percentage"]
            ship_on_time_percentage= product["marketplace_seller"]["rating"]["ship_on_time_percentage"]
            rate = (on_time+ship_on_time_percentage+return_percentage)/3
            rates.append(rate)
            list_1.append((price, lead_time,rate))
        # print(list_1)
        # print(len(list_1))
        max_rate = max(rates)
        # print(max_rate)



        # تاخیر در ارسال به ازای هر 1 روز 4درصد
        #به ازای 1 درصد پایین تر از 1max_rate   درصد از قیمت کاهش میابد

        for info in list_1:

                new_price = info[0]-(info[0]*(info[1]*0.04))
                if info[2]<max_rate:
                    new_price = new_price-(new_price*(max_rate-info[2]*0.01))
                if new_price!=info[0]:
                    print(f"{info[0]}------>{new_price}")