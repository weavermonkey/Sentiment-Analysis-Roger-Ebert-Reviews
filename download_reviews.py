# -*- coding: utf-8 -*-
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import json
import re
from pprint import pprint


camelcase_to_underscore = lambda str: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str).lower().strip('_')

def choose_ebert_reviews():
    driver = webdriver.Firefox()
    driver.get('http://www.rogerebert.com/reviews')
    driver.find_element_by_xpath(
        '/html/body/div[1]/div/section/form/section/fieldset[3]/div[1]/div/ul').click()
    ebert_xpath = '/html/body/div[1]/div/section/form/section/fieldset[3]/div[1]/div/div/ul/li[16]'
    ebert_click = driver.find_element_by_xpath(ebert_xpath).click()
    scroll_count = 0
    len_of_page = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
    match = False
    while (match == False):
        scroll_count += 1
        last_count = len_of_page
        if (scroll_count >= 5):
            break
        time.sleep(0.6)
        len_of_page = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
        if last_count == len_of_page:
            match = True
        print scroll_count
    return driver.page_source


def get_omdb_data(movie_title):
    request_url = 'http://www.omdbapi.com/?apikey=9f6c117a&t=' + movie_title.replace(' ', '+') + '&plot=full'
    omdb_data = json.loads(requests.get(request_url).content)
    return omdb_data


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


def read_review(url):
    review_page_raw = requests.get(url=url)
    cleaned_review = []
    soup_obj = BeautifulSoup(review_page_raw.content, 'html5lib')
    review_paragraphs = soup_obj.find('div', class_='wrapper').find('div', class_='grid content').find_all('section',
                                                                                                           class_='main fixed-rail')[
        0].find_all('article', class_='pad entry')[0].find_all('div')[0].find_all('p')
    raw_review = ''.join(
        [curr_paragraph.replace("\n", "").replace("<p>", "").replace("</p>", "") for
         curr_paragraph in ([review_paragraph.prettify() for review_paragraph in review_paragraphs])]).encode('utf-8')
    review_cleaned = BeautifulSoup(raw_review, 'html5lib', from_encoding='utf-8')

    for x in review_cleaned.body:
        if 'bs4.element.Tag' in str(type(x)):
            cleaned_review.append(x.get_text().encode('utf-8').strip())
        else:
            cleaned_review.append((x.encode('utf-8')).strip())
    return ''.join(cleaned_review)


def read_html_page(home_page):
    movie_data_rows = []
    result_content = choose_ebert_reviews()
    soup_obj = BeautifulSoup(result_content, 'html5lib')
    # print soup_obj
    wrapper_class = soup_obj.find('div', id='review-list')
    for curr_movie_dom in wrapper_class.find_all('figure'):
        movie_details = {'movie_title': '', 'reviewed_by': '', 'ebert_score': 0.0, 'review_url': '', 'review_text': ''}
        star_list = []
        movie_title = curr_movie_dom.find('h5', class_='title').a.get_text()
        movie_critic = curr_movie_dom.find('p', class_='byline').get_text().strip()
        convoluted_rating = curr_movie_dom.find('span', class_='star-rating').find_all('i')
        movie_review_score = get_rating(movie_title, convoluted_rating)
        movie_review_url = home_page + curr_movie_dom.find('h5', class_='title').find_all('a')[0]['href'][8:]
        movie_review = read_review(url=movie_review_url)
        omdb_dict = get_omdb_data(movie_title=movie_title)
        movie_details['movie_title'] = movie_title.strip()
        movie_details['reviewed_by'] = movie_critic.strip()
        movie_details['ebert_score'] = movie_review_score
        movie_details['review_url'] = movie_review_url
        movie_details['review_text'] = movie_review
        for curr_key in omdb_dict.keys():
            movie_details[curr_key] = (omdb_dict[curr_key])
        movie_data_rows.append(movie_details)
        print len(movie_data_rows), movie_details['movie_title']
    return movie_data_rows


def save_webpage_to_csv():
    movie_data_rows = read_html_page('http://www.rogerebert.com/reviews')
    x = pd.DataFrame.from_records(movie_data_rows)
    x.to_csv('twenty_scrolls.csv', index=False, encoding='utf-8')


def clean_df(input_df):
    #print input_df.head()
    snake_case_columns = []
    for curr_col in input_df.columns:
        snake_case_columns.append(camelcase_to_underscore(curr_col))
    input_df.columns = snake_case_columns
    print input_df.columns

clean_df(input_df=pd.read_csv('twenty_scrolls.csv'))