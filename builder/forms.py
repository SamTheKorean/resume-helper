from django import forms

class InputForm(forms.Form):
    input_sentence = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Tell me about your experience, e.g., "I made a web service using Django."',
                'rows': 1,
            }
        )
    )