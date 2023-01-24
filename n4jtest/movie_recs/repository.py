from movie_recs import N4jConnection
from django.conf import settings
import re
from pandas import DataFrame
import pandas as pd
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title
    

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
    return res


def search(movies, title):
    vectorizer = TfidfVectorizer(ngram_range=(1,2))
    tfidf = vectorizer.fit_transform(movies["clean_title"])
    title = clean_title(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    index = np.argpartition(similarity, -1)[-1:]
    results = movies.iloc[index]
    r = results.iat[0, 0]
    
    return r

def find_similar_movies(title):
    ratings = get_ratings()
    movies = get_movies()
    movie_id = search(movies, title)
    
    sim_users = ratings[(ratings["mid"] == movie_id) & (ratings["rating"] > 4)]["uid"].unique()
    sim_user_recs = ratings[(ratings["uid"].isin(sim_users)) & (ratings["rating"] > 4)]["mid"]
    sim_user_recs = sim_user_recs.value_counts() / len(sim_users)

    sim_user_recs = sim_user_recs[sim_user_recs > .10]
    all_users = ratings[(ratings["mid"].isin(sim_user_recs.index)) & (ratings["rating"] > 4)]
    all_user_recs = all_users["mid"].value_counts() / len(all_users["uid"].unique())
    rec_percentages = pd.concat([sim_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["similar", "all"]
    
    rec_percentages["score"] = round(rec_percentages["similar"] / rec_percentages["all"],2)
    rec_percentages = rec_percentages.sort_values("score", ascending=False)
    return rec_percentages.head(10).merge(movies, left_index=True, right_on="id")[["score", "title"]]