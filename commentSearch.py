import praw
import csv

with open('postSearch.csv', mode='w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)

    # creates a reddit instance
    reddit = praw.Reddit(client_id='HFe49kpE24lryrjVxKvl4g',
                         client_secret='gKsY8pbmd-w5k13Tcq-IeHV8bEmzIg',
                         user_agent='Testing_api',
                         username='Famous-Jellyfish8889',
                         password='bachelor.0401')

    # --------------------------------------

    # Choose if you want to search for posts (true) or comments (false)
    post_analysis = True

    # Choose a subreddit you want to analyze
    subreddit = reddit.subreddit('Futurology')

    # --------------------------------------

    # false if you need 'robot' as an extra search word, true if you only look for the keywords
    robotic_subreddit = None

    # keywords you want to search for in a subreddit when looking for posts
    keywords_posts = None

    # keywords you want to search for in a subreddit when looking for comments
    keywords_comments = None

    robot_string = 'robot'

    robotic_subreddit_list = ['loona_robot', 'VectorRobot', 'RobotVacuums', 'litterrobot', 'RobotNews', 'robot',
                              'robots', 'robotics', 'shittyrobots', 'Robot_IRL']

    non_robotic_subreddit_list = ['TechFuture', 'FutureConsequences', 'AutomotiveFuture', 'Future_Technology',
                                  'Futurology', 'Cyberpunk', 'DystopianFuture', 'Automate', 'singularity', 'technology',
                                  'science', 'askphilosophy', 'philosophy', 'psychology', 'EthicalService22', 'moral',
                                  'moraladvice', 'MorallyAmbiguous', 'Alpha_Support', 'Morality',
                                  'EthicalTreatmentofAI', 'ethicalAI', 'AIethics']

    # 26
    keyword_list = ['trust', 'reliable', 'predictable', 'consistent', 'capable', 'skilled', 'competent',
                             'dependable', 'capacity', 'performance', 'ethical', 'respectable', 'principled',
                             'sincere', 'genuine', 'authentic', 'cheat', 'secure', 'fair', 'candid', 'moral',
                             'help', 'aid', 'rely', 'trustworthy', 'honest']

    if subreddit in non_robotic_subreddit_list:
        robotic_subreddit = False
    else:
        robotic_subreddit = True

    print('Robotic Subreddit: ' + str(robotic_subreddit))

    if post_analysis:
        keywords_posts = keyword_list
        keywords_comments = []
    else:
        keywords_posts = []
        keywords_comments = keyword_list

    print('Keywords_Post: ' + str(keywords_posts))
    print('Keywords_Comment: ' + str(keywords_comments))

    # Checks if the keywords are in the comments/replies
    # Returns a list with the matching comments/replies
    def get_comments_from_post(input_comment):

        comment_list = []

        if robotic_subreddit:
            for single_keyword in keywords_comments:
                if single_keyword in input_comment.body:
                    comment_list.append(input_comment.body)
        else:
            if robot_string in input_comment.body:
                if any(single_keyword in input_comment.body for single_keyword in keywords_comments):
                    comment_list.append(input_comment.body)

        return comment_list

    # goes through all the posts with the keyword(s) and prints its comments
    def collect_posts(empty_list):

        if not keywords_posts:  # if you want to search for comments in the entire subreddit
            print('Comment')
            empty_list = subreddit.new(limit=100)
        else:  # if you want to search for posts
            if robotic_subreddit:
                print('post-robotic')
                for keyword123 in keywords_posts:
                    empty_list.extend(subreddit.search(keyword123, limit=None))
            else:
                print('post-not robotic')
                for keyword123 in keywords_posts:
                    empty_list.extend(subreddit.search(f"{keyword123} AND {robot_string}", limit=3))
        return empty_list


    posts = []
    posts = collect_posts(posts)

    counter = 0

    if post_analysis:

        for item in posts:
            post = reddit.submission(item.id)
            csv_writer.writerow([post.title + post.selftext])
            counter += 1
            print(counter)
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
