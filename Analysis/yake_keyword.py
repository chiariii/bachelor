import yake
import pandas as pd
import os
import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

directory_path = "../Data/Future"
csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]

combined_data = []

counter_files = 0
counter_rows = 0

for root, directories, files in os.walk(directory_path):
    for file in files:
        if file.endswith(".csv"):
            csv_file_path = os.path.join(root, file)
            input_csv = pd.read_csv(csv_file_path, header=None)
            input_csv.drop_duplicates(inplace=True)
            text = input_csv.iloc[:, 0].tolist()
            input_yake = ' '.join(text)
            combined_data.append(input_yake)
            counter_files += 1
            counter_rows += len(input_csv)

combined_data = ' '.join(combined_data)

stop = set(stopwords.words('english'))
stop.add('robot')
stop.add('human')
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

# combined_data = clean(combined_data)
print(f"Files included: {counter_files}")
print(f"Rows included: {counter_rows}")

language = 'en'
max_ngram_size = 2
deduplication_thresold = 0.3
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 10

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold,
                                            dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords,
                                            features=None)

keywords = custom_kw_extractor.extract_keywords(combined_data)

for kw in keywords:
    print(kw)
