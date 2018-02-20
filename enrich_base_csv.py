from download_reviews import read_review, get_omdb_data
import pandas as pd
import os
import time
import json
import ast
from pandas.io.json import json_normalize

# base_csv = pd.read_csv('file_with_omdb_attr.csv').to_dict()
base_csv = pd.read_csv('wolololo_df.csv').to_dict()


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
    for i in range(1001, 10781):
        curr_omdb_url = base_csv['omdb_url'][i]
        try:
            curr_omdb_json = get_omdb_data(curr_omdb_url)
            base_csv['omdb_json'][i] = curr_omdb_json
            print curr_omdb_json['Title'], '\n#########################################'
            print i, curr_omdb_url
        except Exception as e:
            print i, curr_omdb_url
            base_csv['omdb_json'][i] = 'Error getting Data From OMDB'
    df_with_omdb_attr = pd.DataFrame(base_csv)
    df_with_omdb_attr.to_csv('file_with_omdb_attr.csv', mode='a', header=False, index=False)


def split_omdb_json_to_columns():
    enriched_csv = base_csv
    for i in range(1000):
        try:
            curr_dict = ast.literal_eval(enriched_csv['omdb_json'][i])
            print i, curr_dict['Title'], len(curr_dict.keys())
            for curr_key in curr_dict:
                if curr_key in enriched_csv:
                    enriched_csv[curr_key][i] = curr_dict[curr_key]
                else:
                    enriched_csv[curr_key] = {}
                    enriched_csv[curr_key][i] = curr_dict[curr_key]
        except:
            pass
    enriched_df = pd.DataFrame(enriched_csv)
    enriched_df.to_csv('wolololo_df.csv', index=False, encoding='utf-8')


def flatten_json_to_columns():
    normalized_dict = base_csv
    json_columns = {}
    for i in range(100):
        for curr_key in base_csv.keys():
            try:
                ast.literal_eval(normalized_dict[curr_key][i])
                json_columns[curr_key] = ''
            except:
                pass
            '''
            if ast.literal_eval(base_csv[curr_key][i]):
                json_columns[curr_key] = True
            else:
                json_columns[curr_key] = False
            '''
    print json_columns


def flatten_ratings_to_columns():
    for i in range(1000):
        try:
            curr_rating_dict = ast.literal_eval(base_csv['Ratings'][i])
            num_reviews = len(curr_rating_dict)
            for i in range(num_reviews):
                curr_source = 'rating_by_' + curr_rating_dict[i]['Source'].lower().replace(' ', '_')
                # print base_csv['movie_title'][i], curr_rating_dict[i]['Source'],':',curr_rating_dict[i]['Value']
                if curr_source in base_csv:
                    base_csv[curr_source][i] = curr_rating_dict[i]['Value']
                else:
                    base_csv[curr_source] = {}
                    base_csv[curr_source][i] = curr_rating_dict[i]['Value']
        except Exception as e:
            print i, e
    normalized_df = pd.DataFrame(base_csv)
    normalized_df.to_csv('normalized_df.csv', index=False)


flatten_ratings_to_columns()
