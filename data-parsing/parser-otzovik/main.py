from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import csv
import re
from fake_useragent import UserAgent
print(UserAgent().chrome)

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)

hrefs = []
review_links = []


def make_string(my_string):
    first = my_string.find(' ')
    my_string = my_string[first + 1:]
    second = my_string.find(' ')
    my_string = my_string[:second]

    return my_string


url = 'https://otzovik.com/reviews/set_magazinov_pyaterochka_russia/'

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

#response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
#print(response)

#print(response.content)

driver.get(url)
time.sleep(10)
html = driver.page_source

amount_of_pages = 251

with open("reviews.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
    file_writer.writerow(
        ["Link", "Name_of_review", "Date", "Advantages", "Disadvantages", "Main_text",
         "Overall_assessment", "Assortment", "Prices", "Delivery",
         "Availability", "Service", "isRecommended"])

    for page in range(194, int(amount_of_pages)):
        print(f'page {page} of {amount_of_pages}')

        time.sleep(1)
        hrefs = []
        review_links = []
        i = 1

        url = 'https://otzovik.com/reviews/set_magazinov_pyaterochka_russia/' + str(page) + '/'
        driver.get(url)

        time.sleep(3)
        reviews_card = driver.find_elements(By.XPATH, "//*[@id='content']/div/div/div/div/div/div/div/div/div/h3/a")

        for review in reviews_card:
            review_link = review.get_attribute('href')
            review_links.append(review_link)


        for review_link in review_links:
            url = review_link
            driver.get(url)
            time.sleep(3)
            print(f'Link {i} of {len(review_links)}')

            try:
                date = driver.find_element(By.XPATH, "//*[@id='content']/div/div/div/div/div[3]/div[1]/div[2]/span/span").text
                #print(date)
            except Exception as ex:
                date = 'NaN'
                print(ex)

            try:
                name_of_review = driver.find_element(By.XPATH, "//*[@id='content']/div/div/div/div/div[3]/div[1]/h1").text
                #print(name_of_review)
            except Exception as ex:
                name_of_review = 'NaN'
                print(ex)

            try:
                advantages = driver.find_element(By.XPATH, "//*[@id='content']/div/div/div/div/div[3]/div[1]/div[4]").text
                #print(advantages)
            except Exception as ex:
                advantages = 'NaN'
                print(ex)

            try:
                disadvantages = driver.find_element(By.XPATH, "//*[@id='content']/div/div/div/div/div[3]/div[1]/div[6]").text
                #print(disadvantages)
            except Exception as ex:
                disadvantages = 'NaN'
                print(ex)

            try:
                main_text_xpath = driver.find_elements(By.XPATH, "//*[@id='content']/div/div/div/div/div[3]/div[1]/div[7]")
                #print(main_text_xpath)
                for main_text in main_text_xpath:
                    main_text1 = main_text.text
                    main_text1 = main_text1.rstrip()
                    re.sub("\n", '', main_text1)
                    print('  ' in main_text1)

                    while "\n" in main_text1:
                        main_text1 = main_text1.replace('\n','')

                    while ";" in main_text1:
                        main_text1 = main_text1.replace(';','')

                    #print(main_text1)
            except Exception as ex:
                main_text1 = 'NaN'
                print(ex)

            try:
                is_recommended = driver.find_element(By.XPATH, "//*[@id='content']/div/div/div/div/div[3]/div[1]/table/tbody[2]/tr[3]/td[2]").text
                print(is_recommended)
            except Exception as ex:
                is_recommended = 'NaN'
                print(ex)

            try:
                overall_assessment = driver.find_element(By.XPATH, "//*[@id='content']/div/div/div/div/div[3]/div[1]/table/tbody[2]/tr[2]/td[2]/abbr[1]").get_attribute(
                    'title')
                #print(overall_assessment)

                assortment = driver.find_element(By.XPATH, "//*[@class='rating-item tooltip-top'][1]").get_attribute(
                    'title')
                assortment = make_string(assortment)
                #print(make_string(assortment))

                prices = driver.find_element(By.XPATH, "//*[@class='rating-item tooltip-top'][2]").get_attribute(
                    'title')

                prices = make_string(prices)
                #print(make_string(prices))

                delivery = driver.find_element(By.XPATH, "//*[@class='rating-item tooltip-top'][3]").get_attribute(
                    'title')
                delivery = make_string(delivery)
                #print(make_string(delivery))

                availability = driver.find_element(By.XPATH, "//*[@class='rating-item tooltip-top'][4]").get_attribute(
                    'title')
                availability = make_string(availability)
                #print(make_string(availability))

                service = driver.find_element(By.XPATH, "//*[@class='rating-item tooltip-top'][5]").get_attribute(
                    'title')
                service = make_string(service)
                #print(make_string(service))

            except Exception as ex:
                overall_assessment = assortment = prices = delivery = availability = service = 'NaN'
                print(ex)

            i += 1

            file_writer.writerow([review_link, name_of_review, date, advantages, disadvantages, main_text1, overall_assessment, assortment, prices, delivery, availability, service, is_recommended])
