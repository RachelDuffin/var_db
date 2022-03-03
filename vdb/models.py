from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

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

def validate_capitalised(value):
    if value != value.capitalize():
        raise ValidationError('Invalid (not capitalised) value: %(value)s',
                              code='invalid',
                              params={'value': value})

validate_hgvsc = RegexValidator(r'^c.[a-zA-Z0-9>_]*$', 'Invalid nomenclature - must follow HGVS nomenclature')
validate_hgvsp = RegexValidator(r'^p.[(][a-zA-Z0-9>_*]*[)]$', 'Invalid nomenclature - must follow HGVS nomenclature')
validate_alphanumeric = RegexValidator(r'^[a-zA-Z0-9]*$', 'Input must contain only letters and numbers')
validate_actg = RegexValidator(r'^[ACTGactg\-]*$', 'Characters must be A, C, T, G or -')


class Variant(models.Model):
    chr = models.CharField(max_length=2, validators=[validate_alphanumeric, validate_capitalised])
    start = models.IntegerField()
    ref = models.CharField(max_length=150, validators=[validate_capitalised, validate_actg])
    alt = models.CharField(max_length=150, validators=[validate_capitalised, validate_actg])
    gene = models.ForeignKey('Gene', on_delete=models.PROTECT)
    build = models.ForeignKey('GenomeBuild', on_delete=models.PROTECT)
    hgvsc = models.CharField(max_length=150, validators=[validate_hgvsc])
    hgvsp = models.CharField(max_length=150, validators=[validate_hgvsp])
    ACMG = models.ManyToManyField('ACMG', blank=True)
    CHOICES = (
        (1, 'Benign'),
        (2, 'Likely benign'),
        (3, 'Variant of uncertain significance'),
        (4, 'Likely pathogenic'),
        (5, 'Pathogenic')
    )

    score = models.PositiveSmallIntegerField(choices=CHOICES, default=3)
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
        return f"{self.chr}:{self.start}:{self.ref}:{self.alt}"


