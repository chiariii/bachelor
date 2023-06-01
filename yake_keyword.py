import yake
import pandas as pd
import os

directory_path = "Data/Ethic_Moral_Psychology/Posts/AIethics_Posts.csv"

input_csv = pd.read_csv(directory_path)
text = input_csv.iloc[:, 0].tolist()
input_yake = ' '.join(text)

language='en'
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
windowSize = 1
numOfKeywords = 10

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
keywords = custom_kw_extractor.extract_keywords(input_yake)

for kw in keywords:
    print(kw)