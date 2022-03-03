from django.shortcuts import render
from .forms import AddVariantForm
from django.shortcuts import redirect
from django.utils import timezone


def variant_new(request):
	if request.method == "POST":
		form = AddVariantForm(request.POST)
		if form.is_valid():
			variant = form.save(commit=False)
#			variant.created_by = request.user
#			variant.created_at = timezone.now()
			variant.save()
#			return redirect('variant_detail', pk=variant.pk)
	else:
		form = AddVariantForm()
	return render(request, 'vdb/variant_new.html', {'form': form})
from .models import Variant

def home(request):
    return render(request, 'vdb/home.html')

def variantlist(request):
    variants = Variant.objects.all()
    return render(request, 'vdb/variant_list.html', {'variants': variants})

