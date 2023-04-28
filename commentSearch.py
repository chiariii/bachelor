import praw

# creates a reddit instance
reddit = praw.Reddit(client_id='HFe49kpE24lryrjVxKvl4g',
                     client_secret='gKsY8pbmd-w5k13Tcq-IeHV8bEmzIg',
                     user_agent='Testing_api',
                     username='Famous-Jellyfish8889',
                     password='bachelor.0401')

# select a subreddit you want to analyze
subreddit = reddit.subreddit('robotics')

# select the keyword(s) you want to look for in the subreddit
keywordsSubreddit = ['trust']

# select the keyword(s) you want to look for in the comments
keywordsComments = ['']


# Checks if the keyword(s) are in the comments or replies and prints the comments
def print_comment(commentar, indent=0):
    if all(keyword in commentar.body for keyword in keywordsComments):
        print('Kommentar: ' + '  ' * indent + commentar.body)
    for reply in commentar.replies:
        if all(keyword in reply.body for keyword in keywordsComments):
            print_comment(reply, indent + 1)


# goes through all the posts with the keyword(s) and prints its comments
for post in subreddit.search(' '.join(keywordsSubreddit)):

    print('Titel:' + post.title)
    submission = reddit.submission(post.id)
    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():
        print_comment(comment)
