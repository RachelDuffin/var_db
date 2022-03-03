from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.forms.models import model_to_dict
from django.contrib import messages
from .models import Variant, Gene
from .forms import AddVariantForm, AddGeneForm
from django.db.models.query_utils import Q


def home(request):
    return render(request, 'vdb/home.html')

  
def variantlist(request):
    variants = Variant.objects.all()
    return render(request, 'vdb/variant_list.html', {'variants': variants})

  
def variantviewer(request, pk):
    variant = model_to_dict(get_object_or_404(Variant, pk=pk))
    ACMG = [model_to_dict(t) for t in variant['ACMG']]
    return render(request, 'vdb/variant_viewer.html', {'variant': variant, 'ACMG': ACMG})

def genelist(request):
    genes = Gene.objects.all()
    return render(request, 'vdb/gene_list.html', {'genes' : genes})
  
  
# form views
def variant_new(request):
    if request.method == "POST":
        form = AddVariantForm(request.POST)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.created_by = request.user
            variant.save()
            messages.success(request, "Variant successfully added to VarDB.")
            return redirect('variant_viewer', pk=variant.pk)
    else:
        form = AddVariantForm()
    return render(request, 'vdb/variant_new.html', {'form': form})


def gene_new(request):
    if request.method == "POST":
        form = AddGeneForm(request.POST)
        if form.is_valid():
            gene = form.save(commit=False)
            gene.save()
            messages.success(request, "Gene successfully added to VarDB.")
            return redirect('variant_new')
    else:
        form = AddGeneForm()
    return render(request, 'vdb/gene_new.html', {'form': form})


def searchdb(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if ':' in q:
            Chr = q.split(':')[0]
            Start = q.split(':')[1]
            variant_list = Variant.objects.filter(chr=Chr, start=Start)
        else:
            variant_list = Variant.objects.filter(Q(chr__icontains=q) | Q(start__icontains=q))
        gene_list = Gene.objects.filter(symbol__icontains=q)

        context = {
            'variant_list': variant_list,
            'gene_list': gene_list,
            'query': q
        }

        return render(request, 'vdb/search_results.html', context)
    else:
        return (request, 'vdb/search_results.html')

