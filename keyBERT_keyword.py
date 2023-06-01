from keybert import KeyBERT
import pandas as pd

# https://towardsdatascience.com/how-to-extract-relevant-keywords-with-keybert-6e7b3cf889ae

directory_path = "Data/Ethic_Moral_Psychology/Posts/AIethics_Posts.csv"

input_csv = pd.read_csv(directory_path)
text = input_csv.iloc[:, 0].tolist()
input_keybert = ' '.join(text)


kw_model = KeyBERT('distilbert-base-nli-mean-tokens')
keywords = kw_model.extract_keywords(input_keybert, keyphrase_ngram_range=(3,3), stop_words='english', use_mmr=True,
                                     diversity=0.8, top_n=10)
print(keywords)

# schöne grafiken erstellen