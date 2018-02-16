# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from download_reviews import get_rating, read_review

initial_url = "https://www.rogerebert.com/reviews?great_movies=0&no_stars=0&order=newest&title=te+rock&filters[great_movies][]=&filters[no_stars][]=&filters[no_stars][]=1&filters[title]=&filters[reviewers]=&filters[genres]=&page="
next_url = initial_url
movie_data_rows = []
i = 0


def save_base_csv(home_page):
    # movie_data_rows = []
    result_content = requests.get(home_page).content
    soup_obj = BeautifulSoup(result_content, 'html5lib')
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
        movie_details['ebert.com_score'] = movie_review_score
        movie_details['ebert.com_review_url'] = movie_review_url
        movie_data_rows.append(movie_details)


while requests.get(next_url).status_code != '404':
    save_base_csv(next_url)
    i += 1
    next_url = initial_url + str(i)
