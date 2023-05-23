import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import os

# Load the data
csv_file_path = os.path.join("Posts", "AIethics_Posts.csv")
data = pd.read_csv(csv_file_path)
data.drop_duplicates(inplace=True)

# Cleaning and preprocessing
stop = set(stopwords.words('english'))
stop.add("i'm")
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


data_clean = [clean(doc).split() for doc in data.iloc[:, 0]]

# preparing document-term matrix
dictionary = corpora.Dictionary(data_clean)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in data_clean]

# running LDA model
Lda = gensim.models.ldamodel.LdaModel
lda_model = Lda(doc_term_matrix, num_topics=5, id2word=dictionary, passes=50)

# results
print(lda_model.print_topics(num_topics=5, num_words=5))

