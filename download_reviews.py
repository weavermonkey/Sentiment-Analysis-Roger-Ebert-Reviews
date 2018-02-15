# -*- coding: utf-8 -*-
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import json
from pprint import pprint

#camelcase_to_underscore = lambda str: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', str).lower().strip('_')
omdb_data = requests.get('http://www.omdbapi.com/?apikey=9f6c117a&t=Basmati+Blues&plot=full')
movie_review_dict = {'movie_title': [], 'reviewed_by': [], 'score': [], 'review_url': [], 'review_text': []
                     }
pprint(movie_review_dict)
y = json.loads(omdb_data.content)
for curr_key in y.keys():
    movie_review_dict[curr_key] = []
pprint(movie_review_dict)

def choose_ebert_reviews():
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
        time.sleep(0.45)
        len_of_page = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
        if last_count == len_of_page:
            match = True


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
    movie_details = movie_review_dict
    result = requests.get(url=home_page)
    result_content = result.content
    soup_obj = BeautifulSoup(result_content, 'html5lib')
    wrapper_class = soup_obj.find('div', id='review-list')
    for curr_movie_dom in wrapper_class.find_all('figure'):
        star_list = []
        movie_title = curr_movie_dom.find('h5', class_='title').a.get_text()
        movie_critic = curr_movie_dom.find('p', class_='byline').get_text().strip()
        convoluted_rating = curr_movie_dom.find('span', class_='star-rating').find_all('i')
        movie_review_score = get_rating(movie_title, convoluted_rating)
        movie_review_url = home_page + curr_movie_dom.find('h5', class_='title').find_all('a')[0]['href'][8:]
        movie_review = read_review(url=movie_review_url)
        omdb_dict = get_omdb_data(movie_title=movie_title)
        movie_details['movie_title'].append(movie_title.strip())
        movie_details['reviewed_by'].append(movie_critic.strip())
        movie_details['score'].append(movie_review_score)
        movie_details['review_url'].append(movie_review_url)
        movie_details['review_text'].append(movie_review)
        for curr_key in omdb_dict.keys():
            if curr_key in movie_details:
                movie_details[curr_key].append(omdb_dict[curr_key])
            else:
                movie_details[curr_key] = []
                movie_details[curr_key].append(omdb_dict[curr_key])
        #print 'Current Movie: ',movie_title,'\n',pprint(movie_details), '\n#####################################'
    #pprint(movie_details)
    return movie_details


def save_webpage_to_csv():
    movie_details = read_html_page('http://www.rogerebert.com/reviews')
    #pprint(movie_details )
    for curr_key in movie_details:
        print curr_key, len( movie_details[curr_key] )
    movie_df = pd.DataFrame(movie_details)
    print movie_df.head()
    movie_df = pd.DataFrame.from_dict(movie_details)

    movie_df.to_csv('roger_ebert_reviews.csv', mode='w', index=False)


save_webpage_to_csv()
