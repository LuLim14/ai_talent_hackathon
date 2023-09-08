from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
import csv
import re

#from fake_useragent import UserAgent
#print(UserAgent().chrome)

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

hrefs = []
review_links = []
urls = ["https://yandex.ru/maps/org/eurospar/110236798747/reviews"
        "/?indoorLevel=0&ll=30.334275%2C59.934759&tab=reviews&z=17.09",
        "https://yandex.ru/maps/org/eurospar/66190683153/reviews/?indoorLevel"
        "=-1&ll=30.346851%2C59.928542&tab=reviews&z=17.09",
        "https://yandex.ru/maps/org/eurospar/72147799884/reviews/?ll=30"
        ".349186%2C59.945703&tab=reviews&z=17.09"]

address = ["Невский просп., 48", "Владимирский просп., 19", "Литейный просп., 12"]

list_amount_of_reviews = [1733, 1167, 762]

# urls = ['https://yandex.ru/maps/org/vkusvill/141001574434/reviews/?ll=30.358780%2C59.944576&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/vkusvill/225353758595/reviews/?ll=30.348620%2C59.936246&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/vkusvill/102212120934/reviews/?ll=30.376235%2C59.938775&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/vkusvill/242735308222/reviews/?indoorLevel=1&ll=30.366740%2C59.930494&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/vkusvill/239339039925/reviews/?indoorLevel=1&ll=30.352870%2C59.928104&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/vkusvill/25549981217/reviews/?ll=30.370513%2C59.928686&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/vkusvill/131086661460/reviews/?ll=30.371968%2C59.920645&tab=reviews&z=17.16',
#          ]
#
# address = ['просп. Чернышевского, 17, Санкт-Петербург',
#            'Литейный просп., 54, Санкт-Петербург',
#            'Суворовский просп., 35, Санкт-Петербург',
#            'Невский просп., 130, Санкт-Петербург',
#            'ул. Марата, 21, Санкт-Петербург',
#            'Невский просп., 111/3, Санкт-Петербург',
#            'Кременчугская ул., 17, корп. 2, Санкт-Петербург',
#            ]
#
# list_amount_of_reviews = [181, 42, 156, 240, 155, 101, 97]

#urls = ["https://yandex.ru/maps/org/pyatyorochka/26017781266/reviews/?ll=30.357924,59.944062&tab=reviews&z=18.13", "https://yandex.ru/maps/org/pyatyorochka/189979809983/reviews/?ll=30.370863,59.929078&tab=reviews&z=17.09", "https://yandex.ru/maps/org/pyatyorochka/213564317684/reviews/?indoorLevel=1&ll=30.367619,59.924980&tab=reviews&z=16.69", "https://yandex.ru/maps/org/pyatyorochka/93682651498/reviews/?ll=30.378741%2C59.942836&tab=reviews&z=17.09", "https://yandex.ru/maps/org/pyatyorochka/1807616597/reviews/?ll=30.348234%2C59.923563&tab=reviews&z=17.09", "https://yandex.ru/maps/org/pyatyorochka/172862519128/reviews/?ll=30.366380%2C59.946185&tab=reviews&z=17.09", "https://yandex.ru/maps/org/pyatyorochka/1586072103/reviews/?ll=30.347875%2C59.939113&tab=reviews&z=17.09"]
# urls = ['https://yandex.ru/maps/org/diksi/76971275236/reviews/?indoorLevel=1&ll=30.365213%2C59.930314&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/diksi/1011988799/reviews/?ll=30.376244%2C59.927757&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/diksi/104097939159/reviews/?indoorLevel=1&ll=30.347111%2C59.926481&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/diksi/1216605146/reviews/?ll=30.355672%2C59.923518&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/diksi/1003029092/reviews/?ll=30.345818%2C59.918485&tab=reviews&z=17.16',
#          'https://yandex.ru/maps/org/diksi/72934277213/reviews/?ll=30.321626%2C59.942895&tab=reviews&z=17.16']

# address = ['Невский просп., 91, Санкт-Петербург',
#            'Перекупной пер., 4, Санкт-Петербург',
#            'Большая Московская ул., 5, Санкт-Петербург',
#            'Лиговский просп., 91, Санкт-Петербург',
#            'ул. Константина Заслонова, 21, Санкт-Петербург',
#            'Миллионная ул., 23, Санкт-Петербург']

# list_amount_of_reviews = [252, 273, 174, 255, 146, 711]

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
#response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
#print(response)
#print(response.content)

with open("reviews.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
    file_writer.writerow(["Address", "Text", "Date", "Stars"])
    for g in range(len(urls)):
        driver.get(urls[g])
        time.sleep(10)
        html = driver.page_source
        a = 0
        i = s = 2

        while len(driver.find_elements(By.XPATH, "//*[@class = 'business-reviews-card-view__review']")) < list_amount_of_reviews[g]:
            iframe = driver.find_element(By.XPATH, "//*[@class = 'business-reviews-card-view__review'][last()]")
            scroll_origin = ScrollOrigin.from_element(iframe)
            ActionChains(driver)\
                .scroll_to_element(iframe)\
                .perform()
            time.sleep(3)
            a += 1
            if a > 20: # in case of incomplete loading of the list of reviews
                break

        list_of_reviews = driver.find_elements(By.XPATH, "//*[@class = 'business-review-view__body-text']")


        for review in list_of_reviews:
            review_text = review.text
            re.sub("\n", '', review_text)

            while "\n" in review_text:
                review_text = review_text.replace('\n', '')

            while ";" in review_text:
                review_text = review_text.replace(';', '')

            list_of_stars = []
            stars = 0

            try:

                for j in range(1, 6):
                    star = driver.find_element(By.XPATH, "(//*[@class = 'business-rating-badge-view__stars'])[" + str(s) + "]/span[" + str(j) + "]")
                    print(star.get_attribute("class"))
                    star_class = star.get_attribute("class")
                    if '_full' in star_class:
                        list_of_stars.append(1)
                    else:
                        list_of_stars.append(0)

                for k in range(len(list_of_stars)):
                    stars += list_of_stars[k]

            except Exception as ex:
                stars = 'NaN'

            data = driver.find_element(By.XPATH, "(//*[@class = 'business-review-view__date'])[" + str(i - 1) + "]/span")
            text_date = data.text

            i += 1
            s += 1

            file_writer.writerow([address[g], review_text, text_date, stars])

        time.sleep(10)
