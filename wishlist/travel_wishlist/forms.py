from django import forms
from .models import Places


class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Places
        fields = ('name', 'visited')