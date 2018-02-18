from download_reviews import read_review
import pandas as pd
import os

base_csv = pd.read_csv('all_review_details.csv').to_dict()
base_csv['rogerebert.com_review_text'] = {}

for i in range(len(base_csv['movie_title'])):
    curr_movie_url = base_csv['ebert.com_review_url'][i]
    print i, curr_movie_url, '\n#############################'
    curr_file_name = os.path.normpath(
        'C:/Users/prog/Desktop/test_github_repo/Sentiment-Analysis-Roger-Ebert-Reviews/reviews/' + str(i + 1) + '.txt')
    if not os.path.exists(curr_file_name):
        curr_review = read_review(url=curr_movie_url)
        with open(curr_file_name, 'w') as file_to_write:
            file_to_write.write(curr_review)
# csv_with_review_df = pd.DataFrame(base_csv)
# csv_with_review_df.to_csv('aioo.csv', index=False, encoding='utf-8')