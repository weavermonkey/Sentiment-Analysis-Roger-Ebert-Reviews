from download_reviews import read_review, get_omdb_data
import pandas as pd
import os
import time

base_csv = pd.read_csv('file_with_omdb_url.csv').to_dict()
base_csv['omdb_json'] = {}



# print pd.read_csv('file_with_reviews.csv').head()

def write_reviews_to_disk():
    for i in range(len(base_csv['movie_title'])):
        curr_movie_url = base_csv['ebert.com_review_url'][i]
        print i, curr_movie_url, '/n#############################'
        curr_file_name = os.path.normpath(
            'C:/Users/prog/Desktop/test_github_repo/Sentiment-Analysis-Roger-Ebert-Reviews/reviews/' + str(
                i + 1) + '.txt')
        if not os.path.exists(curr_file_name):
            curr_review = read_review(url=curr_movie_url)
            with open(curr_file_name, 'w') as file_to_write:
                file_to_write.write(curr_review)


def add_reviews_to_csv():
    reviews_directory = os.path.normpath(
        'C:/Users/prog/Desktop/test_github_repo/Sentiment-Analysis-Roger-Ebert-Reviews/reviews')
    for i in range(10781):  # number of reviews
        curr_review_text = os.path.normpath(
            'C:/Users/prog/Desktop/test_github_repo/Sentiment-Analysis-Roger-Ebert-Reviews/reviews/' + str(
                i + 1) + '.txt')
        base_csv['rogerebert.com_review_text'][i] = open(curr_review_text, 'r').readlines()
    df_with_reviews = pd.DataFrame(base_csv)
    df_with_reviews.to_csv('file_with_reviews.csv', index=False)


def add_omdb_url_to_csv():
    for curr_movie_index in base_csv['movie_title']:
        request_url = 'http://www.omdbapi.com/?apikey=9f6c117a&t=' + base_csv['movie_title'][curr_movie_index].replace(
            ' ', '+') + '&plot=full'
        base_csv['omdb_url'][curr_movie_index] = request_url
    df_with_omdb_url = pd.DataFrame(base_csv)
    df_with_omdb_url.to_csv('file_with_omdb_url.csv', index=False)


def add_omdb_data_to_csv():
    for i in range(2,1001):
        curr_omdb_url = base_csv['omdb_url'][i]
        try:
            curr_omdb_json = get_omdb_data(curr_omdb_url )
            time.sleep(1)
            base_csv['omdb_json'][i] = curr_omdb_json
            print curr_omdb_json['Title'], '\n#########################################'
            print i, curr_omdb_url
        except Exception as e:
            print i, curr_omdb_url
            base_csv['omdb_json'][i] = 'Error getting Data From OMDB'
    df_with_omdb_attr = pd.DataFrame(base_csv)
    df_with_omdb_attr.to_csv('file_with_omdb_attr.csv',index=False)

add_omdb_data_to_csv()