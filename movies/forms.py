from django import forms
from .models import CheckoutFeedback, MoviePetition

class CheckoutFeedbackForm(forms.ModelForm):
    class Meta:
        model = CheckoutFeedback
        fields = ['name', 'feedback']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)',
                'maxlength': 100
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'How did you feel about the checkout process?',
                'rows': 4,
                'required': True
            })
        }
        labels = {
            'name': 'Name (Optional)',
            'feedback': 'How did you feel about the checkout process?'
        }

class MoviePetitionForm(forms.ModelForm):
    class Meta:
        model = MoviePetition
        fields = ['movie_title', 'description']
        widgets = {
            'movie_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter movie title',
                'maxlength': 200
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Why should this movie be added to our catalog?',
                'rows': 4
            })
        }
        labels = {
            'movie_title': 'Movie Title',
            'description': 'Why should this movie be added?'
        }