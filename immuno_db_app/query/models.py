# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models  # type: ignore
import django_tables2 as tables  # type: ignore


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BindingPredictions(models.Model):
    binding_prediction_code = models.BigIntegerField(primary_key=True)
    psm_code = models.ForeignKey('PeptideSpectrumMatches', models.DO_NOTHING, db_column='psm_code', blank=True, null=True)
    hla_code = models.IntegerField(blank=True, null=True)
    prediction_tool = models.TextField(blank=True, null=True)
    prediction_tool_version = models.TextField(blank=True, null=True)
    is_binder = models.BooleanField(blank=True, null=True)
    affinity_score = models.FloatField(blank=True, null=True)
    affinity_rank = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'binding_predictions'


class BlogBlogposts(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    url = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'blog_blogposts'


class DataProcessing(models.Model):
    data_processing_run_code = models.IntegerField(primary_key=True)
    person_data_processing = models.IntegerField(blank=True, null=True)
    processing_software = models.TextField(blank=True, null=True)
    processing_software_version = models.TextField(blank=True, null=True)
    processing_pipeline = models.TextField(blank=True, null=True)
    processing_pipeline_version = models.TextField(blank=True, null=True)
    reference_proteome_version = models.TextField(blank=True, null=True)
    search_engine = models.TextField(blank=True, null=True)
    command_processing = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_processing'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PortfolioProject(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'portfolio_project'


class People(models.Model):
    person_code = models.IntegerField(primary_key=True)
    role = models.TextField()
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'people'


class Projects(models.Model):
    project_code = models.IntegerField(primary_key=True)
    principle_investigator_code = models.ForeignKey(People, models.DO_NOTHING, db_column='principle_investigator_code', blank=True, null=True)
    project_name = models.CharField(max_length=100)
    project_description = models.TextField(blank=True, null=True)
    qbic_project_code = models.CharField(unique=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'projects'


class Proteins(models.Model):
    uniprot_code = models.TextField(primary_key=True)
    protein_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'proteins'


class BiologicalMaterialTypes(models.Model):
    biological_material_code = models.IntegerField(primary_key=True)
    biological_material_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'biological_material_types'


class DiseaseTypes(models.Model):
    disease_code = models.IntegerField(primary_key=True)
    disease_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'disease_types'


class Donors(models.Model):
    donor_code = models.TextField(primary_key=True)
    ncbi_taxonomy_code = models.ForeignKey('OrganismTypes', models.DO_NOTHING, db_column='ncbi_taxonomy_code')

    class Meta:
        managed = False
        db_table = 'donors'


class HlaTypes(models.Model):
    hla_code = models.IntegerField(primary_key=True)
    hla_allele = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'hla_types'


class DonorHla(models.Model):
    donor_hla_code = models.IntegerField(primary_key=True)
    donor_code = models.ForeignKey('Donors', models.DO_NOTHING, db_column='donor_code', blank=True, null=True)
    hla_code = models.ForeignKey('HlaTypes', models.DO_NOTHING, db_column='hla_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'donor_hla'


class DonorHlaView(models.Model):
    donor_code = models.TextField(primary_key=True)
    all_hla_alleles_donor = models.TextField(blank=True, null=True)
    ncbi_taxonomy_code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'donor_hla_view'


class MassSpectrometers(models.Model):
    mass_spectrometer_code = models.SmallIntegerField(primary_key=True)
    mass_spectrometer_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'mass_spectrometers'


class OrganismTypes(models.Model):
    ncbi_taxonomy_code = models.IntegerField(primary_key=True)
    taxonomy_name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'organism_types'


class Samples(models.Model):
    sample_code = models.IntegerField(primary_key=True)
    artificial_sample_code = models.TextField(unique=True)
    project_code = models.ForeignKey(Projects, models.DO_NOTHING, db_column='project_code')
    donor_code = models.ForeignKey(DonorHlaView, models.DO_NOTHING, db_column='donor_code')
    person_sample_acquisition = models.IntegerField(blank=True, null=True)
    qbic_sample_code = models.CharField(unique=True, max_length=10, blank=True, null=True)
    biological_material_name = models.TextField()
    disease_name = models.TextField()
    dignity = models.TextField(blank=True, null=True)
    date_of_sample_acquisition = models.DateField(blank=True, null=True)
    is_metastasis = models.BooleanField(blank=True, null=True)
    is_cell_line = models.BooleanField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    sample_description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'samples'


class MsRuns(models.Model):
    ms_run_code = models.IntegerField(primary_key=True)
    sample_code = models.ForeignKey('Samples', models.DO_NOTHING, db_column='sample_code')
    person_sample_measurement = models.TextField(blank=True, null=True)
    qbic_data_code = models.TextField(blank=True, null=True)
    filename = models.TextField(blank=True, null=True, verbose_name="The FileName")
    replicate_nr = models.SmallIntegerField()
    mass_spectrometer_code = models.ForeignKey(MassSpectrometers, models.DO_NOTHING, db_column='mass_spectrometer_code', blank=True, null=True)
    lcms_method = models.TextField(blank=True, null=True)
    date_of_measurement = models.DateField(blank=True, null=True)
    mhc_class = models.TextField(blank=True, null=True)
    antibody = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ms_runs'


class PeptideSpectrumMatches(models.Model):
    psm_code = models.BigIntegerField(primary_key=True)
    ms_run_code = models.ForeignKey(MsRuns, models.DO_NOTHING, db_column='ms_run_code')
    artificial_peptide_code = models.TextField(unique=True)
    peptide_sequence = models.CharField(max_length=50)
    peptide_length = models.IntegerField(blank=True, null=True)
    retention_time = models.FloatField(blank=True, null=True)
    mass_to_charge = models.FloatField(blank=True, null=True)
    q_value = models.FloatField(blank=True, null=True)
    charge = models.SmallIntegerField(blank=True, null=True)
    search_identifier = models.TextField(blank=True, null=True)
    spectrum_reference = models.TextField(blank=True, null=True)
    ion_frac = models.FloatField(blank=True, null=True)
    delt_cn = models.FloatField(blank=True, null=True)
    delt_lcn = models.FloatField(blank=True, null=True)
    percolator_score = models.FloatField(blank=True, null=True)
    pep = models.FloatField(blank=True, null=True)
    x_corr = models.FloatField(blank=True, null=True)
    sp_score = models.FloatField(blank=True, null=True)
    sp_rank = models.FloatField(blank=True, null=True)
    expectation_value = models.FloatField(blank=True, null=True)
    matched_ions = models.SmallIntegerField(blank=True, null=True)
    total_ions = models.SmallIntegerField(blank=True, null=True)
    num_matched_peptides = models.IntegerField(blank=True, null=True)
    peptide_mass = models.FloatField(blank=True, null=True)
    is_best_spectrum = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peptide_spectrum_matches'


class PeptideSpectrumMatchesMatView(models.Model):
    psm_code = models.BigIntegerField(primary_key=True)
    ms_run_code = models.ForeignKey(MsRuns, models.DO_NOTHING, db_column='ms_run_code')
    artificial_peptide_code = models.TextField(blank=True, null=True)
    peptide_sequence = models.CharField(max_length=50, blank=True, null=True)
    peptide_sequence_mods = models.TextField(blank=True, null=True)
    peptide_length = models.IntegerField(blank=True, null=True)
    retention_time = models.FloatField(blank=True, null=True)
    mass_to_charge = models.FloatField(blank=True, null=True)
    q_value = models.FloatField(blank=True, null=True)
    charge = models.SmallIntegerField(blank=True, null=True)
    search_identifier = models.TextField(blank=True, null=True)
    spectrum_reference = models.TextField(blank=True, null=True)
    ion_frac = models.FloatField(blank=True, null=True)
    delt_cn = models.FloatField(blank=True, null=True)
    delt_lcn = models.FloatField(blank=True, null=True)
    percolator_score = models.FloatField(blank=True, null=True)
    pep = models.FloatField(blank=True, null=True)
    x_corr = models.FloatField(blank=True, null=True)
    sp_score = models.FloatField(blank=True, null=True)
    sp_rank = models.FloatField(blank=True, null=True)
    expectation_value = models.FloatField(blank=True, null=True)
    matched_ions = models.IntegerField(blank=True, null=True)
    total_ions = models.IntegerField(blank=True, null=True)
    num_matched_peptides = models.IntegerField(blank=True, null=True)
    peptide_mass = models.FloatField(blank=True, null=True)
    is_best_spectrum = models.BooleanField(blank=True, null=True)
    peptide_modifications = models.TextField(blank=True, null=True)
    uniprot_ids = models.TextField(blank=True, null=True)
    protein_names = models.TextField(blank=True, null=True)
    hla_allele = models.TextField(blank=True, null=True)
    affinity_rank = models.FloatField(blank=True, null=True)
    prediction_tool = models.TextField(blank=True, null=True)
    is_binder = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'peptide_spectrum_matches_mat_view'


class PeptideProteinMatches(models.Model):
    peptide_protein_matches_code = models.BigIntegerField(primary_key=True)
    psm_code = models.ForeignKey('PeptideSpectrumMatches', models.DO_NOTHING, db_column='psm_code', blank=True, null=True, related_name='peptideproteinmatches')
    uniprot_code = models.ForeignKey('Proteins', models.DO_NOTHING, db_column='uniprot_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peptide_protein_matches'


class PeptideModifications(models.Model):
    peptide_modification_code = models.BigIntegerField(primary_key=True)
    psm_code = models.ForeignKey('PeptideSpectrumMatches', models.DO_NOTHING, db_column='psm_code', blank=True, null=True)
    amino_acid_position = models.SmallIntegerField(blank=True, null=True)
    modification_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'peptide_modifications'


class PeptideModsView(models.Model):
    psm_code = models.ForeignKey('PeptideSpectrumMatches', models.DO_NOTHING, db_column='psm_code', blank=True, null=True)
    peptide_modifications = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'peptide_mods_view'


class ProteinMatchesView(models.Model):
    psm_code = models.ForeignKey('PeptideSpectrumMatches', models.DO_NOTHING, db_column='psm_code', blank=True, null=True)
    uniprot_ids = models.TextField(blank=True, null=True)
    protein_names = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'protein_matches_view'


class SimpleTable(tables.Table):
    class Meta:
        model = PeptideSpectrumMatches


class QueryCount(models.Model):
    peptide_length_min = models.IntegerField(blank=True, null=True)
    peptide_length_max = models.IntegerField(blank=True, null=True)
    biological_material_name = models.TextField(blank=True, null=True)
    disease_name = models.TextField(blank=True, null=True)
    mhc_class = models.TextField(blank=True, null=True)
    dignity = models.TextField(blank=True, null=True)
    is_cell_line = models.BooleanField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'query_count'


class BindingPredictions(models.Model):
    binding_prediction_code = models.BigAutoField(primary_key=True)
    psm_code = models.ForeignKey('PeptideSpectrumMatches', models.DO_NOTHING, db_column='psm_code', blank=True, null=True)
    hla_allele = models.TextField(blank=True, null=True)
    prediction_tool = models.TextField(blank=True, null=True)
    is_binder = models.BooleanField(blank=True, null=True)
    affinity_rank = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'binding_predictions'


class Spectra(models.Model):
    spectrum_code = models.BigAutoField(primary_key=True)
    psm_code = models.ForeignKey(PeptideSpectrumMatches, models.DO_NOTHING, db_column='psm_code', blank=True, null=True)
    spectrum = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spectra'
