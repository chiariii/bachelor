import praw
import csv

# creates a reddit instance
reddit = praw.Reddit(client_id='HFe49kpE24lryrjVxKvl4g',
                     client_secret='gKsY8pbmd-w5k13Tcq-IeHV8bEmzIg',
                     user_agent='Testing_api',
                     username='Famous-Jellyfish8889',
                     password='bachelor.0401')

subreddit_List = ['loona_robot', 'VectorRobot', 'RobotVacuums', 'litterrobot', 'RobotNews', 'robot',
                  'robots', 'robotics', 'shittyrobots', 'Robot_IRL', 'TechFuture', 'FutureConsequences',
                  'AutomotiveFuture', 'Future_Technology', 'Futurology', 'Cyberpunk', 'DystopianFuture', 'Automate',
                  'singularity', 'technology', 'science', 'askphilosophy', 'philosophy', 'psychology',
                  'EthicalService22', 'moral', 'moraladvice', 'MorallyAmbiguous', 'Alpha_Support', 'Morality',
                  'EthicalTreatmentofAI', 'ethicalAI', 'AIethics']

for subreddit123 in subreddit_List:
    subreddit = reddit.subreddit(subreddit123)

    print(subreddit)

    with open(f"{subreddit123}_Comments.csv", mode='w', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)

        # --------------------------------------

        # Choose if you want to search for posts (true) or comments (false)
        post_analysis = False

        # --------------------------------------

        # false if you need 'robot' as an extra search word, true if you only look for the keywords
        robotic_subreddit = None

        # keywords you want to search for in a subreddit when looking for posts
        keywords_posts = None

        # keywords you want to search for in a subreddit when looking for comments
        keywords_comments = None

        robot_string = 'robot'

        # 10
        robotic_subreddit_list = ['loona_robot', 'VectorRobot', 'RobotVacuums', 'litterrobot', 'RobotNews', 'robot',
                                  'robots', 'robotics', 'shittyrobots', 'Robot_IRL']

        # 23
        non_robotic_subreddit_list = ['TechFuture', 'FutureConsequences', 'AutomotiveFuture', 'Future_Technology',
                                      'Futurology', 'Cyberpunk', 'DystopianFuture', 'Automate', 'singularity',
                                      'technology', 'science', 'askphilosophy', 'philosophy', 'psychology',
                                      'EthicalService22', 'moral', 'moraladvice', 'MorallyAmbiguous', 'Alpha_Support',
                                      'Morality', 'EthicalTreatmentofAI', 'ethicalAI', 'AIethics']

        # 26
        keyword_list = ['trust', 'reliable', 'predictable', 'consistent', 'capable', 'skilled', 'competent',
                        'dependable', 'capacity', 'performance', 'ethical', 'respectable', 'principled',
                        'sincere', 'genuine', 'authentic', 'cheat', 'secure', 'fair', 'candid', 'moral',
                        'help', 'aid', 'rely', 'trustworthy', 'honest']

        if subreddit in non_robotic_subreddit_list:
            robotic_subreddit = False
        else:
            robotic_subreddit = True

        if post_analysis:
            keywords_posts = keyword_list
            keywords_comments = []
        else:
            keywords_posts = []
            keywords_comments = keyword_list

        # Checks if the keywords are in the comments/replies
        # Returns a list with the matching comments/replies
        def get_comments_from_post(input_comment):

            comment_list = []

            if robotic_subreddit:
                if any(single_keyword in input_comment.body for single_keyword in keywords_comments):
                    comment_list.append(input_comment.body)
            else:
                if robot_string in input_comment.body:
                    if any(single_keyword in input_comment.body for single_keyword in keywords_comments):
                        comment_list.append(input_comment.body)

            return comment_list

        # goes through all the posts with the keyword(s) and prints its comments
        def collect_posts(empty_list):

            if not keywords_posts:  # if you want to search for comments in the entire subreddit
                empty_list = subreddit.new(limit=None)
            else:  # if you want to search for posts in the subreddit
                if robotic_subreddit:
                    for keyword in keywords_posts:
                        empty_list.extend(subreddit.search(keyword, limit=20))
                else:
                    for keyword in keywords_posts:
                        empty_list.extend(subreddit.search(f"{keyword} AND {robot_string}", limit=None))
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
                    csv_writer.writerow([list_of_comments])

                counter += 1
                print(counter)

    file.close()
