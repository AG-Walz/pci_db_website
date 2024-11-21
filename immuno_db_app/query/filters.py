import django_filters
import logging
import sys
from collections import Counter
from django import forms
from .models import PeptideSpectrumMatchesMatView, DiseaseTypes, BiologicalMaterialTypes, Samples


console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("DB Query")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


class PeptideSpectrumMatchesMatViewFilter(django_filters.FilterSet):
    @classmethod
    def get_unique_values(cls, queryset, name):
        return queryset.values_list(name, flat=True).distinct()

    MHC_CLASS_CHOICES = [
        ('I', 'MHC Class I'),
        ('II', 'MHC Class II'),
    ]

    PEPTIDE_MODIFICATION_CHOICES = [
        ('Oxidation', 'Methionine Oxidation'),
        ('Carbamidomethyl', 'Cysteine Carbamidomethylation'),
    ]

    mhc_class = django_filters.ChoiceFilter(
        field_name='ms_run_code__mhc_class',
        label='MHC Class',
        choices=MHC_CLASS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select-style', 'id': 'id_mhc_class'}),
        empty_label='all classes',
    )
    sequence = django_filters.CharFilter(
        field_name='peptide_sequence',
        method='filter_sequence',
        label='Peptide Sequence',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    modifications = django_filters.ChoiceFilter(
        field_name='peptide_modifications',
        label='Peptide Modifications',
        choices=PEPTIDE_MODIFICATION_CHOICES,
        method='filter_modifications',
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select-style', 'id': 'modifications'}),
        empty_label='all',
    )
    uniprot = django_filters.CharFilter(
        lookup_expr='contains',
        field_name='uniprot_ids',
        label='Uniprot ID',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    biological_material = django_filters.ChoiceFilter(
        field_name='ms_run_code__sample_code__biological_material_name',
        label='Biol. Material',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select-style', 'id': 'id_bio_material'}),
        empty_label='all tissues',
    )
    disease = django_filters.ChoiceFilter(
        field_name='ms_run_code__sample_code__disease_name',
        label='Disease',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select-style', 'id': 'id_disease'}),
        empty_label='all diseases',
    )
    dignity = django_filters.ChoiceFilter(
        field_name='ms_run_code__sample_code__dignity',
        label='Dignity',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'custom-select-style', 'id': 'dignity'}),
        empty_label='all',
    )
    """
    peptide_length_min = django_filters.NumberFilter(
        field_name='peptide_length',
        label='Peptide Length Min',
        lookup_expr='gte',
        min_value=8,
        max_value=30,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min (8-30)'})
    )
    peptide_length_max = django_filters.NumberFilter(
        field_name='peptide_length',
        label='Peptide Length Max',
        lookup_expr='lte',
        min_value=8,
        max_value=30,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max (8-30)'})
    )
    project_code = django_filters.CharFilter(
        field_name='ms_run_code__sample_code__project_code__qbic_project_code',
        label='Project Code',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    donor_code = django_filters.CharFilter(
        field_name='ms_run_code__sample_code__donor_code',
        label='Donor Code',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    """
    include_cell_lines = django_filters.BooleanFilter(
        field_name='ms_run_code__sample_code__is_cell_line',
        method='filter_include_cell_lines',
        widget=forms.CheckboxInput(),  # attrs={'class': 'form-check-input'}
        label='Include Cell Lines',
        required=False
    )
    best_hla_allele = django_filters.CharFilter(
        field_name='hla_allele',
        lookup_expr='icontains',
        label='Best HLA Allele',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    only_include_binders = django_filters.BooleanFilter(
        field_name='is_binder',
        method='filter_only_include_binders',
        widget=forms.CheckboxInput(),  # attrs={'class': 'form-check-input'}
        label='Only Include Binders',
        required=False
    )

    def filter_substring_search(self, queryset, name, value):
        return queryset

    def filter_include_cell_lines(self, queryset, name, value):
        if value is not None:
            filter_field = 'ms_run_code__sample_code__is_cell_line'
            if value:
                return queryset
            else:
                return queryset.filter(**{filter_field: False})
        return queryset

    def filter_only_include_binders(self, queryset, name, value):
        if value:
            return queryset.filter(**{name: True})
        return queryset

    substring_search = django_filters.BooleanFilter(
        method='filter_substring_search',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = PeptideSpectrumMatchesMatView
        fields = ('sequence', 'modifications', 'biological_material', 'mhc_class', 'uniprot', 'disease', 'dignity',)

    def filter_sequence(self, queryset, name, value):
        if self.request.GET.get('substring_search', 'off') == 'on':
            lookup = '__contains'
        else:
            lookup = '__exact'
        return queryset.filter(**{name + lookup: value})


    def filter_modifications(self, queryset, name, value):
        if value:
            return queryset.filter(**{f'{name}__contains': value})
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # manually remove HNSSC1 samples as part of selection
        self.filters['disease'].field.choices = sorted([(x[0], f"{x[0]} ({str(x[1])} samples)") for x in dict(Counter([x['disease_name'] for x in Samples.objects.using('immuno').exclude(donor_code__donor_code__startswith='HNSCC1').values('disease_name')])).items()], key=lambda x: x[1].lower(), reverse=False)
        self.filters['biological_material'].field.choices = sorted([(x[0], f"{x[0]} ({str(x[1])} samples)") for x in dict(Counter([x['biological_material_name'] for x in Samples.objects.using('immuno').exclude(donor_code__donor_code__startswith='HNSCC1').values('biological_material_name')])).items()], key=lambda x: x[1].lower(), reverse=False)
        self.filters['dignity'].field.choices = sorted([(value, value) for value in self.get_unique_values(Samples.objects.all().using('immuno'), 'dignity')], key=lambda x: x[1].lower(), reverse=False)
        self.form.fields['substring_search'] = forms.BooleanField(required=False, label='substring search')
        self.form.fields['include_cell_lines'].initial = False
        self.form.fields['only_include_binders'].initial = False


