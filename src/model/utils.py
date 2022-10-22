import re
import numpy as np
import unidecode
import gensim.downloader as api
from collections import Counter
import spacy
import nltk
from nltk.corpus import stopwords

print("Downloading nltk stop words")
nltk.download('stopwords')
print("Downloading finished")

def vectorize(tokens, model):
    vectors = []
    for token, cnt in Counter(tokens).items():
        if token in model and len(token) > 2 and cnt > 2:
            try:
                vectors.append(model[token])
            except KeyError:
                continue
    if vectors:
        vectors = np.asarray(vectors)
        avg_vec = vectors.mean(axis=0)
        return avg_vec.tolist()
    else:
        return np.zeros(model.vector_size)


def project_data_preparation(text, wv=None):
    reg = re.compile('[^a-zA-Z ]')
    sp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    my_stop = stopwords.words('english') + ['article', 'page', 'papper', 'abstract'
        , 't', 's', 'by', 'awarded', 'conference', 'will', 'of', 'for', 'problem']
    if wv is None:
        wv = api.load('word2vec-google-news-300')
    data = text
    data = ' '.join(reg.sub(' ', unidecode.unidecode(str(data))).lower().strip().split())
    data = [w.lemma_ for w in sp(data) if (w.text not in my_stop)]
    return vectorize(data, wv)
