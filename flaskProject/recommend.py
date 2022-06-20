import pandas as pd
from pymongo import MongoClient
import nltk

import re
import string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download("stopwords")
nltk.download('omw-1.4')
nltk.download('wordnet')
stop = stopwords.words('french')
stop_words_ = set(stopwords.words('french'))
wn = WordNetLemmatizer()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# class RecommenderSystem():
def get_recommendation(top, df_all, scores):
    recommendation = pd.DataFrame(columns=['_id_profiles',  'score'])
    count = 0
    for i in top:
        recommendation.at[count, '_id_profiles'] = df_all['_id'][i]
        recommendation.at[count, 'score'] = scores[count]
        count += 1
    return recommendation


def black_txt(token):
    return token not in stop_words_ and token not in list(string.punctuation) and len(token) > 2


def clean_txt(text):
    clean_text = []
    clean_text2 = []
    print(text)
    text = re.sub("'", "", str(text))
    text = re.sub("(\\d|\\W)+", " ", text)
    text = text.replace("nbsp", "")
    clean_text = [wn.lemmatize(word, pos="v") for word in word_tokenize(text.lower()) if black_txt(word)]
    clean_text2 = [word for word in clean_text if black_txt(word)]
    return " ".join(clean_text2)


def read_mongo(db, collection, query={}, host='host.docker.internal', port=27017, username=None, password=None, no_id=True):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    # Delete the _id

    return df


def _connect_mongo(host, port, username, password, db):
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


if __name__ == '__main__':
    df = read_mongo('prestalink', 'profiles', {})
    df.to_csv('1.csv', index=False)


# def recommender(id):
#     df = read_mongo('Pi', 'links', {})
#     df.to_csv('1.csv', index=False)
#     df_profiles=pd.read_csv('1.csv')
#     cols=['_id']+['education']+['experience']+['location']+['profile_title']
#     df_profiles=df_profiles[cols]
#     df_profiles["text"] = df_profiles["education"].map(str) +" "+ df_profiles["experience"]+ " "+df_profiles['location']+" "+df_profiles['profile_title']
#     cols=['_id']+['text']+['profile_title']
#     df_profiles_final=df_profiles[cols]
#     df_profiles_final['text'] = df_profiles_final['text'].apply(clean_txt)
#     tfidf_vectorizer = TfidfVectorizer()
#     tfidf_profiles = tfidf_vectorizer.fit_transform((df_profiles_final['text'])) #fitting and transforming the vector
#     #u='6060a2d81e12dff4171615c0'
#     u=id
#     index = np.where(df_profiles_final['_id'] == u)[0][0]
#     profile = df_profiles_final.iloc[[index]]
#     print(profile)
#     profile_tfidf = tfidf_vectorizer.transform(profile['text'])
#     cos_similarity_tfidf = map(lambda x: cosine_similarity(profile_tfidf, x),tfidf_profiles)
#     output2 = list(cos_similarity_tfidf)
#     top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:3]
#     list_scores = [output2[i][0][0] for i in top]
#     print(get_recommendation(top,df_profiles_final, list_scores))
#     return pd.DataFrame.to_json(get_recommendation(top,df_profiles_final, list_scores)._id_profiles)

def recommended(profile,number):
    tfidf_vectorizer = TfidfVectorizer()
    df = read_mongo('prestalink', 'profiles', {})
    df.to_csv('1.csv', index=False)
    df_profiles = pd.read_csv('1.csv')
    cols = ['_id'] + ['experience']
    df_profiles = df_profiles[cols]
    df_profiles["text"] = df_profiles["experience"].map(str)
    cols = ['_id'] + ['text']
    df_profiles_final = df_profiles[cols]
    df_profiles_final['text'] = df_profiles_final['text'].apply(clean_txt)
    print(profile)
    tfidf_profiles = tfidf_vectorizer.fit_transform((df_profiles_final['text']))  # fitting and transforming the vector
    profile_tfidf = tfidf_vectorizer.transform([profile])
    cos_similarity_tfidf = map(lambda x: cosine_similarity(profile_tfidf, x), tfidf_profiles)
    output2 = list(cos_similarity_tfidf)
    top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:number]
    list_scores = [output2[i][0][0] for i in top]
    # print(get_recommendation(top, df_profiles_final, list_scores))
    return pd.DataFrame.to_json(get_recommendation(top, df_profiles_final, list_scores)._id_profiles)
    # return pd.DataFrame.to_json(['628947e55b51dfa878e0fa22'])

