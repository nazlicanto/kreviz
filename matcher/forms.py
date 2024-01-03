# matcher/forms.py

from django import forms
from .models import Interest
from account.models import Account

class InterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Account # User model
        fields = ['interests']  
