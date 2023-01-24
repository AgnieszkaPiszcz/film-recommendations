import json
from django.shortcuts import render,redirect
from movie_recs import N4jConnection
from neo4j import Record
from pandas import DataFrame
from django.conf import settings
from movie_recs.repository import *
from pprint import pprint
from django.http import HttpResponse
from .forms import NameMovie



def index(request,rec=None):
    if request.method == 'POST':
        form = NameMovie(request.POST or None,request.FILES or None)
        if form.is_valid():
            movie=form.cleaned_data['your_movie']
            rec=find_similar_movies(movie)
            return render(request,'movies.html',{'movies':rec})

    else:
        form=NameMovie
    
    return render(request,'index.html',{'form':form})

def movies(request):
   return render(request,'movies.html')

 