from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.query_utils import Q

from .models import Variant
from .models import Gene
from .forms import AddVariantForm
from .forms import AddGeneForm


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
    return render(request, 'vdb/gene_list.html', {'genes': genes})
  
  
# form views
@login_required
def variant_new(request):
    if request.method == "POST":
        form = AddVariantForm(request.POST)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.created_by = request.user
            variant.updated_by = request.user
            variant.save()
            form.save_m2m()
            messages.success(request, "Variant successfully added to VarDB.")
            return redirect('variant_viewer', pk=variant.pk)
    else:
        form = AddVariantForm()
    return render(request, 'vdb/variant_new.html', {'form': form})


@login_required
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


@login_required
def update_variant(request, pk=None):
    obj = get_object_or_404(Variant, pk=pk)
    form = AddVariantForm(request.POST or None,
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            variant = form.save(commit=False)
            variant.updated_by = request.user
            variant.save()
            form.save_m2m()
            messages.success(request, "Variant successfully updated.")
            return redirect('variant_viewer', pk=variant.pk)
    return render(request, 'vdb/variant_update.html', {'form': form})


def error_404_view(request, exception):
    data = {}
    return render(request, 'vdb/error_404.html', data)