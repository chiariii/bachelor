from keybert import KeyBERT
import pandas as pd
import os

directory_path = "../Data/Ethic_Moral_Psychology/Posts"
csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]

for csv_file in csv_files:
    csv_file_path = os.path.join(directory_path, csv_file)
    print(csv_file_path)
    input_csv = pd.read_csv(csv_file_path)
    input_csv.drop_duplicates(inplace=True)
    text = input_csv.iloc[:, 0].tolist()
    input_keybert = ' '.join(text)

    kw_model = KeyBERT('distilbert-base-nli-mean-tokens')
    keywords = kw_model.extract_keywords(input_keybert, keyphrase_ngram_range=(3, 3), stop_words='english', use_mmr=True,
                                         diversity=0.8, top_n=10)
    print(keywords)

# Code for creating beautiful graphics goes here
