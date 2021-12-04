import scrapy
import json
import re


class QuotesSpider(scrapy.Spider):
    name = "digispider"

    def start_requests(self):
        urls = [
            "https://www.digikala.com/product/dkp-4979130/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # this function response your request and scrap some information

        data = re.findall("var variants =(.+?);\\n", response.body.decode('utf-8'))
        data = data[0]
        answer = json.loads(data)

        list_1 = []
        rates = []
        prices = []
        colors = set()

        for i in answer:
            product = answer[i]
            price = product["price_list"]["selling_price"] / 10
            prices.append(price)
            lead_time = product["leadTime"]
            cancel_percentage = product["marketplace_seller"]["rating"]["cancel_percentage"]
            return_percentage = product["marketplace_seller"]["rating"]["return_percentage"]
            ship_on_time_percentage = product["marketplace_seller"]["rating"]["ship_on_time_percentage"]
            if product["color"] != []:
                color = product["color"]["title"]

            else:
                color = None
            colors.add(color)

            rate = (cancel_percentage + ship_on_time_percentage + return_percentage) / 3
            rates.append(rate)

            # هر tuple در list_1 به ترتیب تشکیل شده از قیمت,تعداد روز تحویل به مشتری,درصد رضایت و رنگ میباشد
            list_1.append((price, lead_time, rate, color))
        colors = list(colors)
        index = 0
        informations = []
        while index != len(colors):
            list_product_diff_Color = []
            for info in list_1:
                if info[3] == colors[index]:
                    list_product_diff_Color.append(info)
            informations.append(list_product_diff_Color)
            index += 1
        # print(">>>>>>>>>>>>>>>>>", informations)




        your_answer = input("if you want minimum enter m or if you want box enter b?\n").lower()
        if your_answer == "b":
            ans = input("are you in box or not(if yes press y and if no press n?\n").lower()
            if ans == "y":
                #     اگر قیمت خودمان در باکس باشد
                for datas in informations:
                    my_objects = datas[0]
                    color = my_objects[3]
                    my_price = my_objects[0]
                    if len(datas) > 1:
                        second_objects = datas[1]
                        second_price = second_objects[0]
                        print(f"color:{color}")
                        print(f"my price:{my_price}")
                        print(f"second price:{second_price}")
                        print("______________________________")
                    else:
                        print(f"color:{color}")
                        print(f"my price:{my_price}")
                        print("you are only item in this feild.")
                        print("-------------------------------")


            #       # تاخیر در ارسال به ازای هر 1 روز 5درصد
            #         # به ازای 1 درصد پایین ازبالا ترین درصد,1درصد کاهش میابداگر قیمت خودمان در باکس نباشد
            elif ans == "n":
                for datas in informations:
                    box_objects_color = datas[0]
                    box_price = box_objects_color[0]
                    print(f"color:{datas[0][3]}")
                    print(f"box_price:{box_price}")
                    datas.pop(0)
                    for d in datas:
                        # اگر تعداد روز تحویل بیشتر از تعداد روز تحویل داخل باکس باشد
                        if d[1] > box_objects_color[1]:
                            my_price = box_price - (box_price * ((d[1] - box_objects_color[1]) * 0.05))

                            # اگر رضایت مشتری این کالا کمتر از رضایت مشتری داخل باکس باشد
                            if d[2] < box_objects_color[2]:
                                my_price = my_price - (box_price * ((box_objects_color[2] - d[2]) * 0.01))

                            #     # اگر رضایت مشتری این کالا بیشتر از رضایت مشتری داخل باکس باشد
                            elif d[2] > box_objects_color:
                                my_price = my_price + (box_price * ((d[2] - box_objects_color[2]) * 0.01))
                            else:
                                #      اگر رضایت مشتری این کالا برابر رضایت مشتری داخل باکس باشد
                                my_price = my_price
                            print(f"{d[0]}----->{my_price}")

                        # اگر تعداد روز تحویل کمتر از تعداد روز تحویل داخل باکس باشد
                        elif d[1] < box_objects_color[1]:
                            my_price = box_price - (box_price * ((box_objects_color[1] - d[1]) * 0.05))

                            # اگر رضایت مشتری این کالا کمتر از رضایت مشتری داخل باکس باشد
                            if d[2] < box_objects_color[2]:
                                my_price = my_price - (box_price * ((box_objects_color[2] - d[2]) * 0.01))


                            #      اگر رضایت مشتری این کالا بیشتر از رضایت مشتری داخل باکس باشد
                            elif d[2] > box_objects_color:
                                my_price = my_price + (box_price * ((d[2] - box_objects_color[2]) * 0.01))


                            # اگر رضایت مشتری این کالا برابر از رضایت مشتری داخل باکس باشد
                            else:
                                my_price = my_price

                            print(f"{d[0]}----->{my_price}")


                        # اگر تعداد روز تحویل برابر از تعداد روز تحویل داخل باکس باشد
                        else:
                            my_price = box_price

                            # اگر رضایت مشتری این کالا کمتر از رضایت مشتری داخل باکس باشد
                            if d[2] < box_objects_color[2]:
                                my_price = my_price - (box_price * ((box_objects_color[2] - d[2]) * 0.01))

                            #      اگر رضایت مشتری این کالا بیشتر از رضایت مشتری داخل باکس باشد
                            elif d[2] > box_objects_color[2]:
                                my_price = my_price + (box_price * ((d[2] - box_objects_color[2]) * 0.01))

                            #     # اگر رضایت مشتری این کالا برابر از رضایت مشتری داخل باکس باشد
                            else:
                                my_price = my_price
                            print(f"{d[0]}----->{my_price}")
                    print("------------------------")


        #اگر کمترین قیمت را میخواهیم
        elif your_answer == "m":
            for datas in informations:
                prices = []

                for d in datas:
                    prices.append(d[0])
                min_price = min(prices)
                print(f"in color {d[3]} minimum price is {min_price}.your suitable price is {min_price - 1000}")
                print("------------------------")
