from bertopic import BERTopic
import pandas as pd
import numpy as np

tweets_trump = pd.read_csv("Data/Ethic_Moral_Psychology/Comments/AIethics_Comments.csv", engine='python')
tweet_list = tweets_trump.iloc[:, 0].tolist()

topic_model = BERTopic(language="english")

topics, probs = topic_model.fit_transform(tweet_list)

print(topic_model.get_topic_info())


