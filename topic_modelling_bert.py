from datasets import load_dataset
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

data = load_dataset('jamescalam/python-reddit')
data = data.filter(
    lambda x: True if len(x['selftext']) > 30 else 0
)


# we add this to remove stopwords
vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english")

model = BERTopic(
    vectorizer_model=vectorizer_model,
    language='english', calculate_probabilities=True,
    verbose=True
)
topics, probs = model.fit_transform(data)

freq = model.get_topic_info()
freq.head(10)

# https://www.pinecone.io/learn/bertopic/
# https://blog.deepgram.com/python-topic-modeling-with-a-bert-model/
