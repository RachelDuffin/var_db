from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
from .models import Variant

def home(request):
    return render(request, 'vdb/home.html')

def variantlist(request):
    variants = Variant.objects.all()
    return render(request, 'vdb/variant_list.html', {'variants': variants})

def variantviewer(request, pk):
    variant = model_to_dict(get_object_or_404(Variant, pk=pk))
    ACMG = [model_to_dict(t) for t in variant['ACMG']]
    return render(request, 'vdb/variant_viewer.html', {'variant': variant, 'ACMG': ACMG})