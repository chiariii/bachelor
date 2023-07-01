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
    doc = re.sub('# [_]*[a-z]+', '', doc)  # removes hashtags
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


directory_path = ["../Data/RQ2/Matrix/ServiceMech", "../Data/RQ2/Matrix/SocialZoo"]


for dir_path in directory_path:
    # Combine data from all non-empty CSV files
    combined_data = []

    counter_rows = 0

    for root, directories, files in os.walk(dir_path):
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

                counter_rows += len(data)

    print(counter_rows)

    # Preparing document-term matrix
    dictionary = corpora.Dictionary(combined_data)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in combined_data]

    num_top = 0
    num_word = 5

    if counter_rows <= 100:
        num_top = 1
    if 100 < counter_rows <= 500:
        num_top = 5
    if 500 < counter_rows <= 2000:
        num_top = 10
    if counter_rows > 2000:
        num_top = 15

    # Running LDA model
    Lda = gensim.models.ldamodel.LdaModel
    lda_model = Lda(doc_term_matrix, num_topics=num_top, id2word=dictionary, passes=150)

    with open('Results_LDA1.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Data', 'Topics'])
        writer.writerow([dir_path, lda_model.print_topics(num_topics=num_top, num_words=num_word)])
        print(f"{dir_path} is done")
