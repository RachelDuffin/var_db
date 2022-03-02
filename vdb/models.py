from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class GenomeBuild(models.Model):
    build = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.build

class Gene(models.Model):
    symbol = models.CharField(max_length=150, unique=True)
    ncbi = models.IntegerField()
    transcript = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.symbol

class ACMG(models.Model):
    evidence = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.evidence

class Variant(models.Model):
    chr = models.CharField(max_length=2)
    start = models.IntegerField()
    ref =  models.CharField(max_length=150)
    alt = models.CharField(max_length=150)
    gene = models.ForeignKey('Gene', on_delete=models.PROTECT)
    build = models.ForeignKey('GenomeBuild', on_delete=models.PROTECT)
    hgvsc = models.CharField(max_length=150)
    hgvsp = models.CharField(max_length=150)
    ACMG = models.ManyToManyField('ACMG', blank=True)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT,
                                   related_name="var_created_by")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.PROTECT, related_name="var_updated_by")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["build", "chr", "start", "ref", "alt"], name="unique_variant")
        ]

    def __str__(self):
        return self.chr+":"+self.start+":"+self.ref+":"+self.alt
