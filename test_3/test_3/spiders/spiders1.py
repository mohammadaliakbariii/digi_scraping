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
        # this function response your request and scrap some information

        information = re.findall("var variants =(.+?);\\n", response.body.decode('utf-8'))
        information = information[0]
        answer = json.loads(information)
        list_1 = []
        rates = []
        prices = []
        for i in answer:
            product = answer[i]
            price = product["price_list"]["selling_price"]
            prices.append(price)
            lead_time = product["leadTime"]
            cancel_percentage = product["marketplace_seller"]["rating"]["cancel_percentage"]
            return_percentage = product["marketplace_seller"]["rating"]["return_percentage"]
            ship_on_time_percentage = product["marketplace_seller"]["rating"]["ship_on_time_percentage"]
            rate = (cancel_percentage + ship_on_time_percentage + return_percentage) / 3
            rates.append(rate)
            list_1.append((price, lead_time, rate))
        max_rate = max(rates)
        box_price = list_1[0][0]
        box_objects = list_1[0]
        # print(box_objects)
        print(f"box price:{list_1[0][0]}")
        list_1.pop(0)

        # تاخیر در ارسال به ازای هر 1 روز 5درصدد
        # به ازای 1 درصد پایین ازبالا ترین درصد,1درصد کاهش میابد
        your_answer = input("if you want minimum enter m or if you want box enter b?\n").lower()
        if your_answer == "b":
            for info in list_1:

                if box_objects[1] > info[1]:

                    new_price = box_price + (info[0] * (info[1] * 0.05))
                elif box_objects[1] < info[1]:
                    new_price = box_price - (info[0] * (info[1] * 0.05))
                else:
                    new_price = info[0]
                # if info[2] < box_objects[2]:
                #     new_price = new_price - (box_price * ((box_objects[2] - (info[2])) * 0.01))
                # elif info[2] > max_rate:
                #     new_price = new_price + (box_price * ((box_objects[2] - (info[2])) * 0.01))

                print(f"{info[0]}------>{round(new_price, 2)}")


        elif your_answer == "m":
            minimum_price = min(prices)
            print(f"minimum price is {minimum_price}.your suitable price is {minimum_price - 1000}")
