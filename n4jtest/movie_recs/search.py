from sklearn.feature_extraction.text import TfidfVectorizer
from movie_recs.repository import clean_title
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
    
    return results
    