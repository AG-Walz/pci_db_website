import django_tables2 as tables
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe
import logging
from django.core.exceptions import FieldDoesNotExist


console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("DB Query")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


class DivWrappedColumn(tables.Column):
    def __init__(self, classname=None, *args, **kwargs):
        self.classname = classname
        super(DivWrappedColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return mark_safe("<div class='" + self.classname + "' >" + value +"</div>")


class PSMSTable(tables.Table):
    project_code = tables.Column(verbose_name='Project Code', accessor='ms_run_code__sample_code__project_code__qbic_project_code')

    donor_code = tables.Column(verbose_name='Donor Code', accessor='ms_run_code__sample_code__donor_code__donor_code')
    donor_hla_types = DivWrappedColumn(classname='hla_column', verbose_name='Donor HLA Type', accessor='ms_run_code__sample_code__donor_code__all_hla_alleles_donor')

    biological_material = tables.Column(verbose_name='Tissue', accessor='ms_run_code__sample_code__biological_material_name')
    disease_name = tables.Column(verbose_name='Disease', accessor='ms_run_code__sample_code__disease_name')
    dignity = tables.Column(verbose_name='Dignity', accessor='ms_run_code__sample_code__dignity')
    is_metastasis = tables.Column(verbose_name='Metastasis', accessor='ms_run_code__sample_code__is_metastasis')
    is_cell_line = tables.Column(verbose_name='Cell Line', accessor='ms_run_code__sample_code__is_cell_line')
    #treatment = tables.Column(verbose_name='in-vitro treatment', accessor='ms_run_code__sample_code__treatment')

    mhc_class = tables.Column(verbose_name='MHC Class', accessor='ms_run_code__mhc_class')

    peptide_sequence = tables.Column(verbose_name='Peptide Sequence', accessor='peptide_sequence')
    peptide_modifications = tables.Column(verbose_name='Peptide Modifications', accessor='peptide_modifications')
    proteins = DivWrappedColumn(classname='uniprot_column', accessor='uniprot_ids', verbose_name='Uniprot IDs')

    hla_allele = tables.Column(verbose_name='Best HLA Allele', accessor='hla_allele')
    affinity_rank = tables.Column(verbose_name='Affinity % Rank', accessor='affinity_rank')

    show_spectrum_info = tables.Column(
        verbose_name='',
        empty_values=(),
        orderable=False
    )

    class Meta:
        model = PeptideSpectrumMatchesMatView
        template_name = "django_tables2/bootstrap4.html"
        fields = ("peptide_sequence", "hla_allele", "dignity",)  # define the order of columns
        order_by = ("psm_code",)  # add this line to set default ordering


    def render_show_spectrum_info(self, record):
        psm_code = record.pk
        database = self.request.GET.get('database', 'immuno')
        url = reverse('psm_spectrum_info', kwargs={'psm_code': psm_code})
        url_with_db = f"{url}?database={database}"
        return mark_safe(f'<a href="{url_with_db}" class="btn btn-info">Spectrum Info</a>')
