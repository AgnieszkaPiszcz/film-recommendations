from django import forms

class NameMovie(forms.Form):
    your_movie=forms.CharField(label="Movie",max_length=200)