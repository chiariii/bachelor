import praw
import csv

with open('subredditsSearch.csv', mode='w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow((['Title', 'Description', 'Members']))

    # creates a reddit instance
    reddit = praw.Reddit(client_id='HFe49kpE24lryrjVxKvl4g',
                         client_secret='gKsY8pbmd-w5k13Tcq-IeHV8bEmzIg',
                         user_agent='Testing_api',
                         username='Famous-Jellyfish8889',
                         password='bachelor.0401')

    keyword = "robot"

    search_results = reddit.subreddits.search(keyword, limit = None)

    for subreddit in search_results:

        csv_writer.writerow([subreddit.display_name, subreddit.public_description, subreddit.subscribers])

file.close()
