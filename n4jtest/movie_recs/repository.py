from n4jtest import N4jConnection
from django.conf import settings
import re
from pandas import DataFrame
import pandas as pd
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(movies, title):
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(movies["clean_title"])
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = movies.iloc[indices].iloc[::-1]
    r = results.iat[0, 0]
    
    return r


def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

# def convert_ratings(ratings):
#     df = DataFrame(data={})
#     for index, row in ratings.iterrows():
#         df.at[row['uid'], row['mid']] = row['rating']
#     ndf = df.copy()
#     return ndf

# def convert_ratings2(ratings):
#     d = {}
#     for index, row in ratings.iterrows():
#         if d.keys().__contains__(row['uid']):
#             d[row['uid']].update(row['mid'], row['rating'])
#         df.at[row['uid'], row['mid']] = row['rating']
#     ndf = df.copy()
#     return ndf
    

def get_movies():
    res = None
    try: 
        conn = N4jConnection.N4jConnection("bolt://localhost:7687", settings.N4J_USERNAME, settings.N4J_PASSWORD)
        res =  conn.query("MATCH (m:Movie) return m.id as id, m.title as title")
    except Exception as e:
        print("Query failed:", e)
    finally: 
        if conn is not None:
            conn.close()
    if res is not None:
        res["clean_title"] = res["title"].apply(clean_title)
    return res

def get_movie_title_by_id(id):
    res = None
    try: 
        conn = N4jConnection.N4jConnection("bolt://localhost:7687", settings.N4J_USERNAME, settings.N4J_PASSWORD)
        res =  conn.query("MATCH (m:Movie) where m.id =  " + str(id) + " return m.title as title")
    except Exception as e:
        print("Connection failed:", e)
    finally: 
        if conn is not None:
            conn.close()
    if res is not None:
        print(str(res))
    return res

def get_ratings():
    res = None
    try: 
        conn = N4jConnection.N4jConnection("bolt://localhost:7687", settings.N4J_USERNAME, settings.N4J_PASSWORD)
        res =  conn.query("match (u:User)-[r:RATED]->(m:Movie) return u.id as uid, r.rating as rating, m.id as mid")
    except Exception as e:
        print("Query failed:", e)
    finally: 
        if conn is not None:
            conn.close()
    # if res is not None:
    #     res.rename(columns = { "m().prop.id": "id", "m().prop.title": "title" }, inplace=True)
    return res

def find_movies(movie,rate,df):
    data=dict(movie=rate)
    my_df=pd.Series(data=data)
    df=df.loc[my_df.index]
    result=pd.Series(dtype="float64")
    for column in df.columns:
        result[column]=norm(df[column]-my_df)

    result=result[result<=2]
    df2=df2[list(result.index)]
    df2=df2.loc[~df2.index.isin(list(my_df.index))]
    df2=df2.fillna(df2.mean(skipna=True))
    df2=df2.mean(axis=1)
    df2=df2[df2>=4.5]
    return(df2)

def find_similar_movies(title):
    ratings = get_ratings()
    movies = get_movies()
    movie_id = search(movies, title)
    
    similar_users = ratings[(ratings["mid"] == movie_id) & (ratings["rating"] > 4)]["uid"].unique()
    similar_user_recs = ratings[(ratings["uid"].isin(similar_users)) & (ratings["rating"] > 4)]["mid"]
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

    similar_user_recs = similar_user_recs[similar_user_recs > .10]
    all_users = ratings[(ratings["mid"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["mid"].value_counts() / len(all_users["uid"].unique())
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = round(rec_percentages["similar"] / rec_percentages["all"],2)
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="id")[["score", "title"]]