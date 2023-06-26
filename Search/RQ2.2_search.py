import praw
import csv

# creates a reddit instance
reddit = praw.Reddit(client_id='HFe49kpE24lryrjVxKvl4g',
                     client_secret='gKsY8pbmd-w5k13Tcq-IeHV8bEmzIg',
                     user_agent='Testing_api',
                     username='Famous-Jellyfish8889',
                     password='bachelor.0401')

keyword_RQ2 = ['"social robot"', '"service robot"', '"industrial robot"', '"zoomorphic robot"', '"mechanoid robot"',
               '"humanlike robot"']
print(keyword_RQ2)

for keyword_RQ in keyword_RQ2:
    subreddit = reddit.subreddit('all')

    with open(f"{keyword_RQ}_Comments.csv", mode='w', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)

        # --------------------------------------

        # Choose if you want to search for posts (true) or comments (false)
        post_analysis = False

        # --------------------------------------

        # keywords you want to search for in a subreddit when looking for posts
        keywords_posts = None

        # keywords you want to search for in a subreddit when looking for comments
        keywords_comments = None

        # 26
        keyword_trust_list = ['trust', 'reliable', 'predictable', 'consistent', 'capable', 'skilled', 'competent',
                        'dependable', 'capacity', 'performance', 'ethical', 'respectable', 'principled',
                        'sincere', 'genuine', 'authentic', 'cheat', 'secure', 'fair', 'candid', 'moral',
                        'help', 'aid', 'rely', 'trustworthy', 'honest']

        if post_analysis:
            keywords_posts = keyword_trust_list
            keywords_comments = []
        else:
            keywords_posts = []
            keywords_comments = keyword_trust_list

        print("Com")
        print(keywords_comments)
        print("Pos")
        print(keywords_posts)

        # Checks if the keywords are in the comments/replies
        # Returns a list with the matching comments/replies
        def get_comments_from_post(input_comment):

            comment_list = []

            if keyword_RQ in input_comment.body:
                if any(single_keyword in input_comment.body for single_keyword in keywords_comments):
                    comment_list.append(input_comment.body)

            return comment_list

        # goes through all the posts with the keyword(s) and prints its comments
        def collect_posts(empty_list):

            if not keywords_posts:  # if you want to search for comments in the entire subreddit
                empty_list = subreddit.new(limit=None)
            else:  # if you want to search for posts in the subreddit
                for keyword in keywords_posts:
                    empty_list.extend(subreddit.search(f"{keyword_RQ} AND {keyword}", limit=None))
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


