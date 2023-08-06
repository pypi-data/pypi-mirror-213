import spacy
from sklearn.cluster import KMeans
import pandas as pd

nlp = spacy.load('en_core_web_lg')


def get_dummies(categories, n=5):
    #TODO: expose the kmeans arguments here so user can tweak the clustering behavior

    df = pd.DataFrame()

    df['X'] = categories.apply(lambda x: nlp(x).vector)
    X = pd.DataFrame(df['X'].tolist(), index=df['X'].index)

    kmeans = KMeans(n_clusters=n, n_init='auto').fit(X)
    df['smart_category'] = kmeans.predict(X)
    df['smart_category'] = df['smart_category'].apply(lambda x: f'category_{x}')

    smart_dummies = pd.get_dummies(df['smart_category'])
    return smart_dummies



