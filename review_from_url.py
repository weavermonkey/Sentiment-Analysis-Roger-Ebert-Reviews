# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv

initial_url = "https://www.rogerebert.com/reviews?great_movies=0&no_stars=0&order=ol&title=te+rock&filters[great_movies][]=&filters[no_stars][]=&filters[no_stars][]=1&filters[title]=&filters[reviewers]=&filters[genres]=&page="
next_url = initial_url
movie_data_rows = []
i = 0


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


def save_base_csv():
    soup_obj = BeautifulSoup(open('ebert_complete_site.html', 'r'), 'html5lib')
    i = 0
    wrapper_class = soup_obj.find('body').find('div', id='review-list')
    for curr_movie_dom in wrapper_class.find_all('figure'):
        movie_details = {'movie_title': '', 'reviewed_by': '', 'ebert.com_score': 0.0, 'ebert.com_review_url': ''}
        star_list = []
        movie_title = curr_movie_dom.find('h5', class_='title').a.get_text()
        movie_critic = curr_movie_dom.find('p', class_='byline').get_text().strip()
        convoluted_rating = curr_movie_dom.find('span', class_='star-rating').find_all('i')
        movie_review_score = get_rating(movie_title, convoluted_rating)
        movie_review_url = 'http://www.rogerebert.com/reviews' + \
                           curr_movie_dom.find('h5', class_='title').find_all('a')[0]['href'][8:]
        movie_details['movie_title'] = movie_title.strip()
        movie_details['reviewed_by'] = movie_critic.strip()
        movie_details['ebert.com_score'] = str(movie_review_score)
        movie_details['ebert.com_review_url'] = movie_review_url
        i += 1
        with open('all_review_details.csv', 'ab') as file_to_write:
            csv_writer = csv.writer(file_to_write)
            csv_writer.writerow([x.encode('utf-8') for x in movie_details.values()])


def scroll_and_retrieve(num_pages):
    global next_url
    for i in range(num_pages):
        while requests.get(next_url).status_code != '404':
            save_base_csv(next_url)
            i += 1
            next_url = initial_url + str(i)


save_base_csv()
