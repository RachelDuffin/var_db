from django import forms
from .models import Variant, Gene

class AddVariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ('gene', 'chr', 'start', 'ref', 'alt', 'build', 'ACMG', 'score', 'hgvsc', 'hgvsp')

class AddGeneForm(forms.ModelForm):
    class Meta:
        model = Gene
        fields = ('symbol', 'ncbi', 'transcript')
        labels = {
            "symbol": "Gene symbol",
            "ncbi": "NCBI Gene ID",
            "transcript": "RefSeq transcript ID"
        }

