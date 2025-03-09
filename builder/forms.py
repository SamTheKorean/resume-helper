from django import forms

class InputForm(forms.Form):
    input_sentence = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'tell me about your experience', 'rows': 1,}))
