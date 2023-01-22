from django.shortcuts import render,redirect
from n4jtest import N4jConnection
from neo4j import Record
from pandas import DataFrame
from django.conf import settings
from movie_recs.repository import *
from movie_recs.search import search
from pprint import pprint
from django.http import HttpResponse

# Create your views here.
from .forms import NameMovie



def index(request):
    if request.method == 'POST':
        form = NameMovie(request.POST)
        if form.is_valid():
            movie=form.cleaned_data['your_movie']
            rate=form.cleaned_data['your_rate']
            res = get_ratings()
            return find_movies(movie,rate,res)
            # return redirect(movies)
    else:
        form=NameMovie
    
    return render(request,'index.html',{'form':form})

def movies(request):
    
    return render(request,'movies.html')

# def index(request):
#     res = get_ratings()
#     movies = get_movies()
#     s = search(movies, "toy story")
#     print(type(res))
#     print(res.to_json(orient='values'))
#     res.to_json()
    
#     return HttpResponse(res.to_string())

# id usera i jakie filmy ocenił na jakie oceny
 