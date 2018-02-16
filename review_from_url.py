# -*- coding: utf-8 -*-
import re
from selenium import webdriver
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd
import numpy as np
from pprint import pprint
from download_reviews import get_rating

def read_html_page(home_page):
    movie_data_rows = []
    result_content = requests.get(home_page).content
    soup_obj = BeautifulSoup(result_content, 'html5lib')
    #with open('html_content_ebert','w') as html_file:
    #html_file.write(str(soup_obj))
    wrapper_class = soup_obj.find('div', id='review-list')
    for curr_movie_dom in wrapper_class.find_all('figure'):
        movie_details = {'movie_title': '', 'reviewed_by': '', 'ebert_score': 0.0, 'review_url': '', 'review_text': ''}
        star_list = []
        movie_title = curr_movie_dom.find('h5', class_='title').a.get_text()
        movie_critic = curr_movie_dom.find('p', class_='byline').get_text().strip()
        convoluted_rating = curr_movie_dom.find('span', class_='star-rating').find_all('i')
        movie_review_score = get_rating(movie_title, convoluted_rating)
        movie_review_url = home_page + curr_movie_dom.find('h5', class_='title').find_all('a')[0]['href'][8:]
        #movie_review = read_review(url=movie_review_url)
        # omdb_dict = get_omdb_data(movie_title=movie_title)
        movie_details['movie_title'] = movie_title.strip()
        movie_details['reviewed_by'] = movie_critic.strip()
        #movie_details['ebert_score'] = movie_review_score
        movie_details['review_url'] = movie_review_url
        #movie_details['review_text'] = movie_review
        movie_details['omdb_url'] = movie_review_url
        # for curr_key in omdb_dict.keys():
        #    movie_details[curr_key] = (omdb_dict[curr_key])
        movie_data_rows.append(movie_details)
        print len(movie_data_rows), movie_details['movie_title']
    print len(movie_data_rows)
base_url = 'https://www.rogerebert.com/reviews?great_movies=0&no_stars=0&order=newest&title=te+rock&filters[great_movies][]=&filters[no_stars][]=&filters[no_stars][]=1&filters[title]=&filters[reviewers]=&filters[genres]=&page='
sort_order = '&sort[order]=newest'

for i in range(10):
    request_url = base_url + str(i) + sort_order
    read_html_page(request_url)