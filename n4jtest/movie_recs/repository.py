from n4jtest import N4jConnection
from django.conf import settings

def get_movies():
    res = None
    try: 
        conn = N4jConnection.N4jConnection("bolt://localhost:7687", settings.N4J_USERNAME, settings.N4J_PASSWORD)
        res =  conn.query("MATCH (m:Movie) return *")
    except Exception as e:
        print("Query failed:", e)
    finally: 
        if conn is not None:
            conn.close()
    if res is not None:
        res.rename(columns = { "m().prop.id": "id", "m().prop.title": "title" }, inplace=True)
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
        res =  conn.query("match (u:User)-[r:RATED]->(m:Movie) return u.id as uid, r.rating as rating, m.id as mid limit 10")
    except Exception as e:
        print("Query failed:", e)
    finally: 
        if conn is not None:
            conn.close()
    # if res is not None:
    #     res.rename(columns = { "m().prop.id": "id", "m().prop.title": "title" }, inplace=True)
    return res