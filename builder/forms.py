from django import forms
from .models import Resume

class InputForm(forms.Form):
    input_sentence = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'please enter a sentense from your resume', 'rows': 1,}))
