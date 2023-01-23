from django import forms

class NameMovie(forms.Form):
    your_movie=forms.CharField(required=True,label="Movie",max_length=200)
   