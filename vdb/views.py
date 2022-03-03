from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.forms.models import model_to_dict
from django.contrib import messages
from .models import Variant
from .forms import AddVariantForm, AddGeneForm

    
def home(request):
    return render(request, 'vdb/home.html')

  
def variantlist(request):
    variants = Variant.objects.all()
    return render(request, 'vdb/variant_list.html', {'variants': variants})

  
def variantviewer(request, pk):
    variant = model_to_dict(get_object_or_404(Variant, pk=pk))
    ACMG = [model_to_dict(t) for t in variant['ACMG']]
    return render(request, 'vdb/variant_viewer.html', {'variant': variant, 'ACMG': ACMG})
  
  
# form views
def variant_new(request):
	if request.method == "POST":
		form = AddVariantForm(request.POST)
		if form.is_valid():
			variant = form.save(commit=False)
			variant.created_by = request.user
			variant.save()
      form.save_m2m()
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

def update_variant(request, pk=None):
    obj = get_object_or_404(Variant, pk=pk)
    form = AddVariantForm(request.POST or None,
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            variant = form.save(commit=False)
            variant.save()
            form.save_m2m()
            messages.success(request, "Variant successfully updated.")
            return redirect('variant_viewer', pk=variant.pk)
    return render(request, 'vdb/variant_update.html', {'form': form})
