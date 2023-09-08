import document
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
import csv
import re
import requests

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

list_of_links = []
hrefs = []
review_links = []

for i in range(1, 3):
    main_url = 'https://2gis.ru/spb/search/Пятёрочка%2C%20супермаркет%20центральный%20район/page/' + str(i) + '?m=30.340917%2C59.930937%2F14.89'

    driver.get(main_url)
    time.sleep(5)
    list_of_links_xpath = driver.find_elements(By.XPATH, "//*[@id='root']/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div[1]/a")

    for link in list_of_links_xpath:
        list_of_links.append(link.get_attribute('href'))

with open("reviews.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
    file_writer.writerow(["Address", "Text", "Stars", "Date"])
    for link in list_of_links:
        k = 4
        d = 1
        driver.get(link)

        print(link)
        try:
            address = driver.find_element(By.XPATH, "(//*[@class = '_2lcm958'])[5]").get_attribute("textContent")
        except Exception as ex:
            address = 'NaN'

        time.sleep(5)
        review_link = link[:link.find('?')] + '/tab/reviews'

        driver.get(review_link)
        time.sleep(5)
        amount = driver.find_element(By.XPATH, "//*[@id='root']/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div[3]/div/a/span[1]").text
        print(int(amount))
        time.sleep(5)
        df = 0
        while len(driver.find_elements(By.XPATH, "//*[@class = '_11gvyqv']/div[3]/div/a")) != int(amount):
            df += 1
            iframe = driver.find_element(By.XPATH, "//*[@class = '_11gvyqv'][last()]")
            scroll_origin = ScrollOrigin.from_element(iframe)
            ActionChains(driver)\
                .scroll_to_element(iframe)\
                .perform()
            time.sleep(3)
            length = len(driver.find_elements(By.XPATH, "//*[@class = '_11gvyqv']/div[3]/div/a"))
            print(f'len list = {length}, всего = {int(amount)}')
            if df > 15:
                amount = len(driver.find_elements(By.XPATH, "//*[@class = '_11gvyqv']/div[3]/div/a"))
                break
        print('End scrolling')

        list_of_reviews = driver.find_elements(By.XPATH, "//*[@class = '_49x36f']/a")
        print(len(list_of_reviews))

        for review in list_of_reviews:
            print(f'review = {review}')
            review_text = review.get_attribute("textContent")
            print(f'review text = {review_text}')
            re.sub("\n", '', review_text)

            while "\n" in review_text:
                review_text = review_text.replace('\n', '')

            while ";" in review_text:
                review_text = review_text.replace(';', '')

            stars = driver.find_elements(By.XPATH, "//*[@id='root']/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div[" + str(k) + "]/div[1]/div/div[2]/div/div[1]/span")
            amount_stars = len(stars)

            date_xpath = driver.find_element(By.XPATH, "(//*[@class = '_4mwq3d'])[" + str(d) + "]")
            date = date_xpath.get_attribute("textContent")

            k += 1
            d += 1
            file_writer.writerow([address, review_text, amount_stars, date])

        time.sleep(10)
