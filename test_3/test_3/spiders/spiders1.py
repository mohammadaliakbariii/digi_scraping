import scrapy
import json
import re


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
          "https://www.digikala.com/product/dkp-6351381",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        answ = re.findall("var variants =(.+?);\\n", response.body.decode('utf-8'))
        answ = answ[0]
        answ_1 = json.loads(answ)

        list_1 = []
        for i in answ_1:
            a = answ_1[i]
            price = a["price_list"]["selling_price"]
            final_percentage = a["marketplace_seller"]["rating"]["final_percentage"]
            is_exist_in_warhouse = a["isExistsInWarehouse"]
            # print(price)
            # print(final_percentage)
            list_1.append((price, final_percentage, is_exist_in_warhouse))
        print(list_1)
        excellent_percentege = list_1[0][1]
        # print(excellent_percentege)
        print(len(list_1))
        # به ازای هر یه درصد کاهش رضایت مشتری نسبت به رضایت کالای مشتری که در باکس است 0.01 درصد کاهش میابد
        # اگر در انبار دیجیکالا موجود نباشد 0.08 از قیمت باید کاهش یابد

        for item in list_1:
            # for i in list_1:
            #     if len(i)>1:
            #         list_1.remove(i)
            if item[1] >= excellent_percentege:
                if item[2] == True:
                    print(f"{item[0]}----->{item[0]}")
                else:
                    print(f"{item[0] - (item[0] * 0.08)}")
                    print(f"{item[0]}----->{item[0]}")
            elif item[1] < excellent_percentege:
                if item[2] == True:
                    percent_low = excellent_percentege - item[1]
                    low = percent_low * 0.01
                    print(f"{item[0]}----->{item[0] - low}")
                else:
                    percent_low = excellent_percentege - item[1]
                    low = percent_low * 0.01
                    print(f"{item[0]}----->{item[0] - low - (item[0] * 0.08)}")






# class entity:
#     def __init__(self, price, final_percentage, ):
#         self.price = price
#         self.final_percentage = final_percentage
#
#     def make_dictionary(self):
#         dictionary = {"pice": self.price,
#                       "final_price": self.final_percentage}
