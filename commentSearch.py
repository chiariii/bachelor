import praw
import csv

with open('postSearch.csv', mode='w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow((['Index', 'Title', 'Text', 'Comments']))

    # creates a reddit instance
    reddit = praw.Reddit(client_id='HFe49kpE24lryrjVxKvl4g',
                         client_secret='gKsY8pbmd-w5k13Tcq-IeHV8bEmzIg',
                         user_agent='Testing_api',
                         username='Famous-Jellyfish8889',
                         password='bachelor.0401')

    # select a subreddit you want to analyze
    subreddit = reddit.subreddit('robotics')

    # select the keyword(s) you want to look for in the subreddit
    # leave empty if you want to search all comments in the subreddit
    keywordsSubreddit = ['trust', 'reliable']

    # select the keyword(s) you want to look for in the comments
    # leave empty if you want all comments from a post
    keywordsComments = []

    # false if you need 'robot' as an extra search word, true if you only look for the keywords
    robotic_subreddit = False

    # Checks if the keyword(s) are in the comment/replies
    # Returns a list with the matching comment/replies
    def get_comments_from_post(input_comment):

        comment_list = []

        if all(keyword in input_comment.body for keyword in keywordsComments):
            comment_list.append(input_comment.body)
        for reply in input_comment.replies:
            if all(keyword in reply.body for keyword in keywordsComments):
                comment_list += get_comments_from_post(reply)

        return comment_list


    # goes through all the posts with the keyword(s) and prints its comments

    limitAll = None
    limitKeywords = None

    posts = []

    if not keywordsSubreddit:  # if you want to search for comments in the entire subreddit
        posts = subreddit.new(limit=limitAll)
    else:  # if you want to search for posts
        if robotic_subreddit:
            for keyword123 in keywordsSubreddit:
                posts.extend(subreddit.search(keyword123, limit=limitAll))
        else:
            for keyword123 in keywordsSubreddit:
                posts.extend(subreddit.search(f"{keyword123} AND robot", limit=limitAll))



    counter = 0

    for item in posts:

        post = reddit.submission(item.id)
        post.comments.replace_more(limit=None)

        list_of_comments = []

        for comment in post.comments.list():
            list_of_comments.extend(get_comments_from_post(comment))

        counter += 1

        # csv_writer.writerow([counter, post.title, post.selftext, *list_of_comments])
        csv_writer.writerow([counter, post.title])

file.close()
