import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string
# import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from keybert import KeyBERT
import yake

# https://medium.com/@y.s.yoon/nlp-illustration-in-python-extracting-keywords-e9c4a6e0a267

# nltk.download('punkt')   # Required for tokenization
# nltk.download('wordnet') # Required for lemmatization


df = pd.read_csv('AIethics_Comments.csv')

df['word_count'] = df.iloc[:, 0].str.split().str.len()

# Histogram
plt.figure(figsize=(15, 4))  # Size
plt.hist(df['word_count'])  # Plot
plt.rcParams['font.size'] = 20  # Font size
plt.ylabel("Frequency", fontsize=20)  # Y label
plt.xlabel("Word Count", fontsize=20)  # X label
plt.title("Histogram", fontsize=30)  # Title
plt.show()

# Kernel Density Plot
plt.figure(figsize=(15, 4))  # Size
ax = sns.kdeplot(df['word_count'],  # Plot
                 color="Red", fill=True)
ax.set_ylabel("Density", fontsize=20)  # Y label
ax.set_xlabel("Word Count", fontsize=20)  # X label
plt.title(
    "Word Count - Kernel Density Estimation",
    fontsize=30)  # title
plt.show()

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


df.iloc[:, 0] = df.iloc[:, 0].apply(clean_texts)  # View the first 5 rows

# Instantiate Word Cloud
wc = WordCloud(width=2400,
               height=1500,
               min_font_size=10,
               background_color='white')

# Generate a word cloud
plt.figure(figsize=(24, 6))
lease_wc = wc.generate(df.iloc[:, 0].str.cat(sep=" "))
plt.xticks([])
plt.yticks([])
# Save the word cloud as an image file
lease_wc.to_file('word_cloud.png')

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

# Instantiate TF-IDF
vectorizer = TfidfVectorizer()  # Fit the data
tfidf = vectorizer.fit_transform(df.iloc[:, 0])  # Create a dataframe of TFIDF
tfidf_df = pd.DataFrame(tfidf[0].T.todense(),
                        index=vectorizer.get_feature_names_out(),
                        columns=["TF-IDF"])  # Sort
tfidf_df = tfidf_df.sort_values('TF-IDF', ascending=False)  # Bar Plot
tfidf_df[:20].plot.bar(title="Top 30 TF-IDF Words")
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

# Instantiate (set n-word groupings hyperparameters to 2)
kw_extractor = yake.KeywordExtractor(n=2)  # Extract keywords and scores from each disclosure
keywords = df.iloc[:, 0].apply(kw_extractor.extract_keywords)  # Extract scores from the YAKE output
text = []
for listi in keywords:
    for component in listi:
        text.append(str(component[0]))

# Bar plot - Create a dataframe of the most common 20 words
common_words = pd.DataFrame(Counter(text).most_common(20))
common_words.columns = ('Word', 'Count')  # Plot a bar chart of the most common 20 words
sns.barplot(x=common_words['Word'], y=common_words['Count'])
plt.xticks(rotation='vertical')
plt.title("Key Word Count Yake", fontsize=20)
plt.show()
