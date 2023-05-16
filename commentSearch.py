import praw
import csv
import re

with open('postSearch.csv', mode='w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    # creates a reddit instance
    reddit = praw.Reddit(client_id='HFe49kpE24lryrjVxKvl4g',
                         client_secret='gKsY8pbmd-w5k13Tcq-IeHV8bEmzIg',
                         user_agent='Testing_api',
                         username='Famous-Jellyfish8889',
                         password='bachelor.0401')

    # false if you need 'robot' as an extra search word, true if you only look for the keywords
    robotic_subreddit = None

    robot_string = 'robot'

    robotic_subreddit_list = ['loona_robot', 'VectorRobot', 'RobotVacuums', 'litterrobot', 'RobotNews', 'robot',
                              'robots', 'robotics', 'shittyrobots', 'Robot_IRL']

    non_robotic_subreddit_list = ['TechFuture', 'FutureConsequences', 'AutomotiveFuture', 'Future_Technology',
                                  'Futurology', 'Cyberpunk', 'DystopianFuture', 'Automate', 'singularity', 'technology',
                                  'science', 'askphilosophy', 'philosophy', 'psychology', 'EthicalService22', 'moral',
                                  'moraladvice', 'MorallyAmbiguous', 'Alpha_Support', 'Morality',
                                  'EthicalTreatmentofAI', 'ethicalAI', 'AIethics']

    # select a subreddit you want to analyze
    subreddit = reddit.subreddit('Futurology')

    # false if comments should be analyzed true if posts should be analyzed
    post_analysis = False

    if subreddit in non_robotic_subreddit_list:
        robotic_subreddit = False
    elif subreddit in robotic_subreddit_list:
        robotic_subreddit = True

    # select the keyword(s) you want to look for in the subreddit
    # leave empty if you want to search all comments in the subreddit

    # keywords_subreddit = ['trust', 'reliable', 'predictable', 'consistent', 'capable', 'skilled', 'competent',
    #                       'dependable', 'capacity', 'performance', 'ethical', 'respectable', 'principled',
    #                       'sincere', 'genuine', 'authentic', 'cheat', 'secure', 'fair', 'candid', 'moral',
    #                       'help', 'aid', 'rely', 'trustworthy', 'honest']

    keywords_subreddit = []

    # select the keyword(s) you want to look for in the comments
    # leave empty if you want all comments from a post
    keywords_comments = ['trust', 'reliable', 'predictable', 'consistent', 'capable', 'skilled', 'competent',
                         'dependable', 'capacity', 'performance', 'ethical', 'respectable', 'principled',
                         'sincere', 'genuine', 'authentic', 'cheat', 'secure', 'fair', 'candid', 'moral',
                         'help', 'aid', 'rely', 'trustworthy', 'honest']

    # keywords_comments = []

    # Checks if the keyword(s) are in the comment/replies
    # Returns a list with the matching comment/replies
    def get_comments_from_post(input_comment):

        comment_list = []

        if robotic_subreddit:
            for single_keyword in keywords_comments:
                if single_keyword in input_comment.body:
                    comment_list.append(input_comment.body)
        else:
            if robot_string in input_comment.body:
                for single_keyword in keywords_comments:
                    if single_keyword in input_comment.body:
                        comment_list.append(input_comment.body)

        return comment_list

    # goes through all the posts with the keyword(s) and prints its comments
    def collect_posts(empty_list):

        if not keywords_subreddit:  # if you want to search for comments in the entire subreddit
            empty_list = subreddit.new(limit=100)
        else:  # if you want to search for posts
            if robotic_subreddit:
                for keyword123 in keywords_subreddit:
                    empty_list.extend(subreddit.search(keyword123, limit=None))
            else:
                for keyword123 in keywords_subreddit:
                    empty_list.extend(subreddit.search(f"{keyword123} AND {robot_string}", limit=None))
        return empty_list


    posts = []
    posts = collect_posts(posts)

    if post_analysis:

        for item in posts:
            post = reddit.submission(item.id)
            csv_writer.writerow([post.title + post.selftext])
    else:
        for item in posts:
            post = reddit.submission(item.id)
            post.comments.replace_more(limit=None)

            list_of_comments = []

            for comment in post.comments.list():
                list_of_comments.extend(get_comments_from_post(comment))
            if len(list_of_comments) > 0:
                csv_writer.writerow([*list_of_comments])

file.close()
