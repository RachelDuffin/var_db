from django.contrib import admin
from .models import GenomeBuild, Gene, ACMG, Variant

admin.site.register(GenomeBuild)
admin.site.register(Gene)
admin.site.register(ACMG)
admin.site.register(Variant)
