import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import os
import re

# Load the data
csv_file_path = os.path.join("Posts", "AIethics_Posts.csv")
data = pd.read_csv(csv_file_path)
data.drop_duplicates(inplace=True)

# Cleaning and preprocessing
stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean(doc):
    doc = re.sub(r'http\S+', '', doc)  # filters links
    doc = re.sub('\s +', '', doc)  # removes extra whites
    doc = re.sub('[^a-zA-Z0-9 ]+', '', doc)  # removes special characters
    doc = re.sub('<.* ? >', '', doc)  # removes html tags
    doc = re.sub('\w\.-]+ @ [\w\.-]+\.\w +', '', doc)  # removes email addresses
    doc = re.sub('# [_]*[a-z]+','', doc)  # removes hashtags
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


data_clean = [clean(doc).split() for doc in data.iloc[:, 0]]

# preparing document-term matrix
dictionary = corpora.Dictionary(data_clean)
# more methods for doc2bow (only bag of words) maybe find a newer?

doc_term_matrix = [dictionary.doc2bow(doc) for doc in data_clean]

# running LDA model
Lda = gensim.models.ldamodel.LdaModel
lda_model = Lda(doc_term_matrix, num_topics=2, id2word=dictionary,
                passes=100)  # higher number of passes -> more precise?

# results
print(lda_model.print_topics(num_topics=2, num_words=3))


