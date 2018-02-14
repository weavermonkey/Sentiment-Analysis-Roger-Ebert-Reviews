from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
from pprint import pprint


def choose_ebert_reviews():
    # driver = webdriver.Firefox()
    driver = webdriver.Firefox()
    driver.get('http://www.rogerebert.com/reviews')
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/section/form/section/fieldset[3]/div[1]/div/ul').click()
    ebert_xpath = '/html/body/div[1]/div/section/form/section/fieldset[3]/div[1]/div/div/ul/li[16]'
    ebert_click = driver.find_element_by_xpath(ebert_xpath).click()


def scroll_to_bottom(webpage):
    driver = webdriver.Firefox()
    driver.get(webpage)
    len_of_page = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
    match = False
    while (match == False):
        last_count = len_of_page
        time.sleep(0.43)
        len_of_page = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
        if last_count == len_of_page:
            match = True


def get_rating(movie_name, star_param):
    movie_rating = 0.0
    star_list = [i.prettify().replace("\n", "").replace("<i class=\"", "").replace("></i>", "").replace("\"", "") for i
                 in star_param]
    for curr_rating in star_list:
        if curr_rating == 'icon-star-full':
            movie_rating += 1
        else:
            movie_rating += 0.5
    return movie_rating


def read_html_page(home_page):
    movie_review_dict = {}
    result = requests.get(url=home_page)
    result_content = result.content
    soup_obj = BeautifulSoup(result_content, 'html5lib')
    wrapper_class = soup_obj.find('div', id='review-list')
    for x in wrapper_class.find_all('figure'):
        star_list = []
        movie_title = x.find('h5', class_='title').a.get_text()
        movie_critic = x.find('p', class_='byline').get_text()
        convoluted_rating = x.find('span', class_='star-rating').find_all('i')
        movie_review_score = get_rating(movie_title, convoluted_rating)
        print type(x.find('h5', class_='title').find_all('a'))


read_html_page('http://www.rogerebert.com/reviews')
