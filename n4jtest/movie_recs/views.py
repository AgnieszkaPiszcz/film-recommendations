from django.shortcuts import render
from n4jtest import N4jConnection
from neo4j import Record
from pandas import DataFrame
from django.conf import settings
from movie_recs.repository import *
from movie_recs.search import search
from pprint import pprint

# Create your views here.

from django.http import HttpResponse


def index(request):
    res = get_ratings()
    movies = get_movies()
    s = search(movies, "toy story")
    print(type(res))
    print(res.to_json(orient='values'))
    res.to_json()
    
    return HttpResponse(res.to_string())

# id usera i jakie filmy ocenił na jakie oceny
 