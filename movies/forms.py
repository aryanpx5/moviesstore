
from django import forms
from .models import CheckoutFeedback

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