from django.shortcuts import render
from n4jtest import N4jConnection
from neo4j import Record

# Create your views here.

from django.http import HttpResponse


def index(request):
    conn = N4jConnection.N4jConnection("bolt://localhost:7687", "neo4j", "adminadmin")
    res =  conn.query("MATCH p=()-[r:RATED]->() RETURN p LIMIT 5")
    return HttpResponse(str(res))
