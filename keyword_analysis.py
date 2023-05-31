import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from keybert import KeyBERT
import yake
# https://medium.com/@y.s.yoon/nlp-illustration-in-python-extracting-keywords-e9c4a6e0a267

# nltk.download('punkt')   # Required for tokenization
# nltk.download('wordnet') # Required for lemmatization

df = pd.read_csv('AIethics_Comments.csv')
df['word_count'] = df.iloc[:, 0].str.split().str.len()

# Descriptive stats
# print(df['word_count'].describe())

# Instantiate
lemmatizer = WordNetLemmatizer()  # Create our own stop words
stop = set(stopwords.words('english'))
exclist = string.punctuation + string.digits  # Exclusion list of punctuations and numbers


# Function to perform preprocessing
def clean_texts(input_text):
    # Convert to lower cases
    input_text = input_text.lower()
    # Remove punctuations and numbers
    input_text = input_text.translate(str.maketrans("", "", exclist))
    # Replace certain words
    input_text = input_text.replace("leased", "lease")
    # Tokenization
    tokens = word_tokenize(input_text)
    # Lemmatization
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    # Remove stop words
    tokens = [token for token in tokens if token not in stop]
    # Join tokens
    clean_text = " ".join(tokens)
    # Return the output
    return clean_text  # Apply the function to all disclosures


df.iloc[:, 0] = df.iloc[:, 0].apply(clean_texts)

plt.figure(figsize=(20, 25))

# Bar plot - Create a corpus of disclosures
corpus = []
for disclosures in df.iloc[:, 0].tolist():
    for word in disclosures.split():
        corpus.append(word)  # Bar plot - Create a dataframe of the most common 30 words
common_words = pd.DataFrame(Counter(corpus).most_common(20))
common_words.columns = ('Word', 'Count')  # Plot a bar chart of the most common 20 words
sns.set(font_scale=1.5)
sns.barplot(x=common_words['Word'], y=common_words['Count'])
plt.xticks(rotation='vertical')
plt.title("Key Word Count", fontsize=20)
plt.show()

# keybert
kw_model = KeyBERT()  # Extract keywords
keywords = df.iloc[:, 0].apply(kw_model.extract_keywords)  # Print the keywords in the first two disclosures
# Extract keywords from the KeyBERT output
text = []
for listi in keywords:
    for component in listi:
        text.append(str(component[0]))  # Bar plot - Create a dataframe of the most common 20 words
common_words = pd.DataFrame(Counter(text).most_common(20))
common_words.columns = ('Word', 'Count')  # Plot a bar chart of the most common 20 words
sns.barplot(x=common_words['Word'], y=common_words['Count'])
plt.xticks(rotation='vertical')
plt.title("KeyBERT Top 20 ", fontsize=20)
plt.show()

# YAKE
kw_extractor = yake.KeywordExtractor()
text = df.iloc[:, 0].apply(clean_texts)
language = "en"
max_ngram_size = 3
deduplication_threshold = 0.9
numOfKeywords = 20

custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                            top=numOfKeywords, features=None)

keywords = custom_kw_extractor.extract_keywords(text)

for kw in keywords:
    print(kw)

# keywords = df.iloc[:, 0].apply(kw_extractor.extract_keywords)
# text = []
# for listi in keywords:
#     for component in listi:
#         text.append(str(component[0]))
#
# # Bar plot - Create a dataframe of the most common 20 words
# common_words = pd.DataFrame(Counter(text).most_common(20))
# common_words.columns = ('Word', 'Count')  # Plot a bar chart of the most common 20 words
# sns.barplot(x=common_words['Word'], y=common_words['Count'])
# plt.xticks(rotation='vertical')
# plt.title("Yake", fontsize=20)
# plt.show()
