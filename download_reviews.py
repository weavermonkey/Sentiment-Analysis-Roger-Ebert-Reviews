from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Firefox()


def choose_ebert_reviews():
    # driver = webdriver.Firefox()
    driver.get('http://www.rogerebert.com/reviews')
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/section/form/section/fieldset[3]/div[1]/div/ul').click()
    ebert_xpath = '/html/body/div[1]/div/section/form/section/fieldset[3]/div[1]/div/div/ul/li[16]'
    ebert_click = driver.find_element_by_xpath(ebert_xpath).click()


def scroll_to_bottom(webpage):
    driver.get(webpage)
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True


scroll_to_bottom('http://www.rogerebert.com/reviews')
