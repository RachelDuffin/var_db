from django import forms
from django.forms import CharField
from .models import Variant

class AddVariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ('gene', 'chr', 'start', 'ref', 'alt', 'build', 'ACMG', 'score', 'hgvsc', 'hgvsp')


