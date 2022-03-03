
from django.shortcuts import render, get_object_or_404
from .forms import AddVariantForm
from django.shortcuts import redirect
from django.utils import timezone
from .models import Variant
from django.forms.models import model_to_dict

def variant_new(request):
    if request.method == "POST":
        form = AddVariantForm(request.POST)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.save()
            form.save_m2m()
            return redirect('variant_viewer', pk=variant.pk)
    else:
        form = AddVariantForm()
    return render(request, 'vdb/variant_new.html', {'form': form})

def update_variant(request, pk=None):
    obj = get_object_or_404(Variant, pk=pk)
    form = AddVariantForm(request.POST or None,
                        request.FILES or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            variant = form.save(commit=False)
            variant.save()
            form.save_m2m()
            return redirect('variant_viewer', pk=variant.pk)
    return render(request, 'vdb/variant_update.html', {'form': form})

    
def home(request):
    return render(request, 'vdb/home.html')

def variantlist(request):
    variants = Variant.objects.all()
    return render(request, 'vdb/variant_list.html', {'variants': variants})

def variantviewer(request, pk):
    variant = model_to_dict(get_object_or_404(Variant, pk=pk))
    ACMG = [model_to_dict(t) for t in variant['ACMG']]
    return render(request, 'vdb/variant_viewer.html', {'variant': variant, 'ACMG': ACMG})
