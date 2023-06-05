import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
import os
import re
import csv

# Cleaning and preprocessing functions
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


# Combine data from all non-empty CSV files
combined_data = []

# Set the directory path where the CSV files are located
directory_path = "../Data"

for root, directories, files in os.walk(directory_path):
    for file in files:
        if file.endswith(".csv"):
            # Load the data
            csv_file_path = os.path.join(root, file)
            data = pd.read_csv(csv_file_path, header=None)
            data.drop_duplicates(inplace=True)

            # Clean and preprocess the data
            data_clean = [clean(doc).split() for doc in data.iloc[:, 0]]

            # Add cleaned data to combined_data
            combined_data.extend(data_clean)

# Preparing document-term matrix
dictionary = corpora.Dictionary(combined_data)
doc_term_matrix = [dictionary.doc2bow(doc) for doc in combined_data]

num = 30

# Running LDA model
Lda = gensim.models.ldamodel.LdaModel
lda_model = Lda(doc_term_matrix, num_topics=num, id2word=dictionary, passes=150)

# Print the results
print(lda_model.print_topics(num_topics=num, num_words=5))

# with open('Results_LDA.csv', 'a', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Data', 'Topics'])
#     writer.writerow([directory_path, lda_model.print_topics(num_topics=num, num_words=3)])









