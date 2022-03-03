from django import forms
from .models import Variant, Gene

class AddVariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ('gene', 'chr', 'start', 'ref', 'alt', 'build', 'ACMG', 'score', 'hgvsc', 'hgvsp')
        labels = {
            "hgvsc": "HGVSc",
            "hgvsp": "HGVSp"
        }

    def __init__(self, *args, **kwargs):
        super(AddVariantForm, self).__init__(*args, **kwargs)
        self.fields['chr'].widget.attrs['placeholder'] = "17"
        self.fields['start'].widget.attrs['placeholder'] = "41256184"
        self.fields['ref'].widget.attrs['placeholder'] = "G"
        self.fields['alt'].widget.attrs['placeholder'] = "T"
        self.fields['hgvsc'].widget.attrs['placeholder'] = "c.396C>A"
        self.fields['hgvsp'].widget.attrs['placeholder'] = "p.Asn132Lys"

class AddGeneForm(forms.ModelForm):
    class Meta:
        model = Gene
        fields = ('symbol', 'ncbi', 'transcript')
        labels = {
            "symbol": "Gene symbol",
            "ncbi": "NCBI Gene ID",
            "transcript": "RefSeq transcript ID"
        }
    def __init__(self, *args, **kwargs):
        super(AddGeneForm, self).__init__(*args, **kwargs)
        self.fields['symbol'].widget.attrs['placeholder'] = "HBB"
        self.fields['ncbi'].widget.attrs['placeholder'] = "3043"
        self.fields['transcript'].widget.attrs['placeholder'] = "NM_000518.5"
