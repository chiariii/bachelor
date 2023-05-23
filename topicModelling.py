import re
import gensim
from gensim.utils import simple_preprocess
import nltk
import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords
import gensim.corpora as corpora
from pprint import pprint

if __name__ == '__main__':

    # load file
    papers = pd.read_csv('beispiel.csv')

    # remove punctuation/lowercasing
    papers['Sentences_processed'] = \
        papers['Header'].map(lambda x: re.sub('[,\.!?]', '', x))

    papers['Sentences_processed'] = \
        papers['Sentences_processed'].map(lambda x: x.lower())

    # wordcloud
    long_string = ','.join(list(papers['Sentences_processed'].values))
    wordcloud = WordCloud(background_color='white', max_words=5000, contour_width=3, contour_color='steelblue')
    wordcloud.generate(long_string)
    wordcloud.to_file('wordcloud.png')

    # more preprocessing
    nltk.download('stopwords')

    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])


    def sent_to_words(sentences):
        for sentence in sentences:
            yield gensim.utils.simple_preprocess(str(sentence), deacc=True)


    def remove_stopwords(texts_input):
        return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts_input]


    data = papers.Sentences_processed.values.tolist()
    data_words = list(sent_to_words(data))

    data_words = remove_stopwords(data_words)

    # actual lda
    id2word = corpora.Dictionary(data_words)
    texts = data_words
    corpus = [id2word.doc2bow(text) for text in texts]

    num_topics = 3
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics=num_topics)

    pprint(lda_model.print_topics())





