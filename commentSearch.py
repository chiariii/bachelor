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
keywordsSubreddit = []

# select the keyword(s) you want to look for in the comments
keywordsComments = ['trust']


# Checks if the keyword(s) are in the comments or replies and prints the comments
def print_comment(comment_to_print, indent=0):
    if all(keyword in comment_to_print.body for keyword in keywordsComments):
        print('comment: ' + '  ' * indent + comment_to_print.body)
    for reply in comment_to_print.replies:
        if all(keyword in reply.body for keyword in keywordsComments):
            print_comment(reply, indent + 1)


# goes through all the posts with the keyword(s) and prints its comments

if not keywordsSubreddit:
    posts = subreddit.new(limit=None)
else:
    posts = subreddit.search(' '.join(keywordsSubreddit))

for post in posts:

    print('title:' + post.title)
    submission = reddit.submission(post.id)
    submission.comments.replace_more(limit=None)

    for comment in submission.comments.list():
        print_comment(comment)
