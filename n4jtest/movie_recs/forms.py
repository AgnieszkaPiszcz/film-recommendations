from django import forms

class NameMovie(forms.Form):
    your_movie=forms.CharField(required=True,label="Movie",max_length=200)
    your_rate=forms.FloatField(required=True,max_value=5.0,min_value=1.0,widget=forms.NumberInput(attrs={'id': 'NameMovie', 'step': "0.01"}))