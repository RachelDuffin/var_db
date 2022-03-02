from django import forms
from django.forms import CharField
from .models import Variant

class AddVariantForm(forms.ModelForm):
    gene = CharField()
    hgvsc = CharField()
    hgvsp = CharField()
    class Meta:
        model = Variant
        fields = ('chr', 'start', 'ref', 'alt', 'build', 'ACMG', 'score')


