from download_reviews import read_review
import pandas as pd
import os

base_csv = pd.read_csv('all_review_details.csv').to_dict()
base_csv['rogerebert.com_review_text'] = {}


def write_reviews_to_disk():
    for i in range(len(base_csv['movie_title'])):
        curr_movie_url = base_csv['ebert.com_review_url'][i]
        print i, curr_movie_url, '/n#############################'
        curr_file_name = os.path.normpath(
            'C:/Users/prog/Desktop/test_github_repo/Sentiment-Analysis-Roger-Ebert-Reviews/reviews/' + str(i + 1) + '.txt')
        if not os.path.exists(curr_file_name):
            curr_review = read_review(url=curr_movie_url)
            with open(curr_file_name, 'w') as file_to_write:
                file_to_write.write(curr_review)

def add_reviews_to_csv():
    reviews_directory = os.path.normpath('C:/Users/prog/Desktop/test_github_repo/Sentiment-Analysis-Roger-Ebert-Reviews/reviews')
    for i in range(10781): #number of reviews
        curr_review_text = os.path.normpath('C:/Users/prog/Desktop/test_github_repo/Sentiment-Analysis-Roger-Ebert-Reviews/reviews/' + str(i+1) + '.txt')
        base_csv['rogerebert.com_review_text'][i] = open(curr_review_text,'r').readlines()
        print i,curr_review_text,'\n############################################'
    df_with_reviews = pd.DataFrame(base_csv)
    df_with_reviews.to_csv('file_with_reviews.csv',index=False)

add_reviews_to_csv()