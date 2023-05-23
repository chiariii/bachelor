import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from wordcloud import WordCloud

# load data
data = pd.read_csv('DystopianFuture_Posts.csv')

# Cleaning and preprocessing
stop = set(stopwords.words('english'))
# stop.add("i'm")
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


data_clean = [clean(doc).split() for doc in data['Header']]

# preparing document-term matrix
dictionary = corpora.Dictionary(data_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in data_clean]

# running LDA model
Lda = gensim.models.ldamodel.LdaModel
lda_model = Lda(doc_term_matrix, num_topics=10, id2word=dictionary, passes=50)

# results
print(lda_model.print_topics(num_topics=10, num_words=5))

