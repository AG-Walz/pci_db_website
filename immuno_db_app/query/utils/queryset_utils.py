import sys

from django.db import connections, transaction
from ..models import PeptideSpectrumMatchesMatView, QueryCount


def append_context_for_dl(request, context):
    """
    Append context for download
    :param request: GET or POST request
    :param context: context dictionary
    :return: context dictionary appended with parsed query information
    """
    if request.method == 'GET' or request.method == 'POST':
        if request.GET.get('substring_search', None) or request.POST.get('substring_search', None):
            substring_search = request.GET.get('substring_search', request.POST.get('substring_search', None))
            substring_search = 'on' == substring_search
            context['substring_search'] = substring_search
        else:
            context['substring_search'] = False

        if request.GET.get('sequence', None) or request.POST.get('sequence', None):
            context['peptide_sequence'] = request.GET.get('sequence', request.POST.get('sequence', "all"))
        else:
            context['peptide_sequence'] = 'all'

        if request.GET.get('mhc_class', None) or request.POST.get('mhc_class', None):
            context['mhc_class'] = request.GET.get('mhc_class', request.POST.get('mhc_class', "all"))
        else:
            context['mhc_class'] = 'all'

        if request.GET.get('modifications', None) or request.POST.get('modifications', None):
            context['peptide_modifications'] = request.GET.get('modifications',
                                                               request.POST.get('modifications', "all"))
        else:
            context['peptide_modifications'] = 'all'

        if request.GET.get('uniprot', None) or request.POST.get('uniprot', None):
            context['uniprot'] = request.GET.get('uniprot', request.POST.get('uniprot', "all"))
        else:
            context['uniprot'] = 'all'

        if request.GET.get('disease', None) or request.POST.get('disease', None):
            context['disease'] = request.GET.get('disease', request.POST.get('disease', "all"))
        else:
            context['disease'] = 'all'

        if request.GET.get('biological_material', None) or request.POST.get('biological_material', None):
            context['biological_material'] = request.GET.get('biological_material',
                                                             request.POST.get('biological_material', "all"))
        else:
            context['biological_material'] = 'all'

        if request.GET.get('dignity', None) or request.POST.get('dignity', None):
            context['dignity'] = request.GET.get('dignity', request.POST.get('dignity', "all"))
        else:
            context['dignity'] = 'all'

        if request.GET.get('peptide_length_min', None) or request.POST.get('peptide_length_min', None):
            context['peptide_length_min'] = request.GET.get('peptide_length_min',
                                                            request.POST.get('peptide_length_min', None))
        else:
            context['peptide_length_min'] = None

        if request.GET.get('peptide_length_max', None) or request.POST.get('peptide_length_max', None):
            context['peptide_length_max'] = request.GET.get('peptide_length_max',
                                                            request.POST.get('peptide_length_max', None))
        else:
            context['peptide_length_max'] = None

        if request.GET.get('project_code', None) or request.POST.get('project_code', None):
            context['project_code'] = request.GET.get('project_code', request.POST.get('project_code', "all"))
        else:
            context['project_code'] = 'all'

        if request.GET.get('donor_code', None) or request.POST.get('donor_code', None):
            context['donor_code'] = request.GET.get('donor_code', request.POST.get('donor_code', "all"))
        else:
            context['donor_code'] = 'all'

        if request.GET.get('include_cell_lines', None) or request.POST.get('include_cell_lines', None):
            include_cell_lines = request.GET.get('include_cell_lines', request.POST.get('include_cell_lines', "all"))
            context['include_cell_lines'] = 'on' == include_cell_lines
        else:
            context['include_cell_lines'] = False

    return context


def generate_filtered_query(request, database_name):
    """
    Generates a filtered queryset based on the request parameters
    :param request: GET or POST request
    :param database_name: name of the database to query
    :return: queryset
    """
    filter_dict = {}
    if request.method == 'GET' or request.method == 'POST':
        if request.GET.get('substring_search', None) or request.POST.get('substring_search', None):
            substring_search = request.GET.get('substring_search', request.POST.get('substring_search', None))
            substring_search = 'on' == substring_search
        else:
            substring_search = False

        if request.GET.get('sequence', None) or request.POST.get('sequence', None):
            # add substring filter to filter dict if substring search is on
            if substring_search:
                filter_dict['peptide_sequence__contains'] = request.GET.get('sequence',
                                                                            request.POST.get('sequence', None))
            else:
                filter_dict['peptide_sequence'] = request.GET.get('sequence', request.POST.get('sequence', None))

        if request.GET.get('mhc_class', None) or request.POST.get('mhc_class', None):
            filter_dict['ms_run_code__mhc_class'] = request.GET.get('mhc_class', request.POST.get('mhc_class', None))

        if request.GET.get('modifications', None) or request.POST.get('modifications', None):
            filter_dict['peptide_modifications__contains'] = request.GET.get('modifications',
                                                                             request.POST.get('modifications', None))

        if request.GET.get('uniprot', None) or request.POST.get('uniprot', None):
            filter_dict['uniprot_ids__contains'] = request.GET.get('uniprot', request.POST.get('uniprot', None))

        if request.GET.get('disease', None) or request.POST.get('disease', None):
            filter_dict['ms_run_code__sample_code__disease_name'] = request.GET.get('disease',
                                                                                    request.POST.get('disease', None))

        if request.GET.get('biological_material', None) or request.POST.get('biological_material', None):
            filter_dict['ms_run_code__sample_code__biological_material_name'] = request.GET.get('biological_material',
                                                                                                request.POST.get(
                                                                                                    'biological_material',
                                                                                                    None))

        if request.GET.get('dignity', None) or request.POST.get('dignity', None):
            filter_dict['ms_run_code__sample_code__dignity'] = request.GET.get('dignity',
                                                                               request.POST.get('dignity', None))

        if request.GET.get('peptide_length_min', None) or request.POST.get('peptide_length_min', None):
            filter_dict['peptide_length__gte'] = request.GET.get('peptide_length_min',
                                                                 request.POST.get('peptide_length_min', None))

        if request.GET.get('peptide_length_max', None) or request.POST.get('peptide_length_max', None):
            filter_dict['peptide_length__lte'] = request.GET.get('peptide_length_max',
                                                                 request.POST.get('peptide_length_max', None))

        if request.GET.get('project_code', None) or request.POST.get('project_code', None):
            filter_dict['ms_run_code__sample_code__project_code__qbic_project_code'] = request.GET.get('project_code',
                                                                                                       request.POST.get(
                                                                                                           'project_code',
                                                                                                           None))

        if request.GET.get('donor_code', None) or request.POST.get('donor_code', None):
            filter_dict['ms_run_code__sample_code__donor_code'] = request.GET.get('donor_code',
                                                                                  request.POST.get('donor_code', None))

        include_cell_lines = request.GET.get('include_cell_lines', request.POST.get('include_cell_lines', 'off'))
        if include_cell_lines == 'on':
            pass
        else:
            filter_dict['ms_run_code__sample_code__is_cell_line'] = False

    # define accessors for columns
    psm_code = 'psm_code'
    peptide_sequence = 'peptide_sequence'
    proteins = 'uniprot_ids'
    peptide_modifications = 'peptide_modifications'
    mhc_class = 'ms_run_code__mhc_class'
    filename = 'ms_run_code__filename'
    biological_material = 'ms_run_code__sample_code__biological_material_name'
    disease_name = 'ms_run_code__sample_code__disease_name'
    dignity = 'ms_run_code__sample_code__dignity'
    is_metastasis = 'ms_run_code__sample_code__is_metastasis'
    is_cell_line = 'ms_run_code__sample_code__is_cell_line'
    treatment = 'ms_run_code__sample_code__treatment'
    donor_code = 'ms_run_code__sample_code__donor_code__donor_code'
    donor_hla_types = 'ms_run_code__sample_code__donor_code__all_hla_alleles_donor'
    project_code = 'ms_run_code__sample_code__project_code__qbic_project_code'
    peptide_length = 'peptide_length'

    cols_for_query = [psm_code, peptide_sequence, proteins, peptide_modifications, mhc_class, filename,
                      biological_material, disease_name, dignity, is_metastasis, is_cell_line, treatment, donor_code,
                      donor_hla_types, project_code, peptide_length]

    queryset = PeptideSpectrumMatchesMatView.objects.using(database_name).all().values(*cols_for_query).order_by(
        'psm_code').filter(**filter_dict)

    return queryset


def get_queryset_count_with_timeout(queryset, timeout=1000, database='immuno'):
    """
    Get count of queryset with timeout  - if timeout occurs, return -1
    :param queryset: queryset to count
    :param timeout: timeout in ms
    :param database: name of database to use e.g. 'immuno'
    :return: count of queryset or -1 if timeout occurred
    """
    try:
        with transaction.atomic(using=database):
            with connections[database].cursor() as cursor:
                cursor.execute(f"SET LOCAL statement_timeout TO {timeout};")
                count = queryset.count()
            return count
    except Exception as e:
        print(e, file=sys.stderr)
        return -1


def get_queryset_count(queryset, query_context, database='immuno', timeout=1000):
    """
    Get count of queryset
    :param queryset: queryset to count
    :param query_context: context dict
    :param database: database name to use e.g. 'immuno'
    :return: string representation of count (or '<' added to count if timeout occurred and cache was used)
    """
    count = get_queryset_count_with_timeout(queryset, timeout=timeout, database=database)
    if count == -1:
        return ""
    else:
        return f"{count:,} peptides found"


def get_cacheable_status(context):
    """
    Check if query is cacheable
    :param context: context dict
    :return: bool
    """
    exclude_columns = [
        "peptide_sequence",
        "peptide_modifications",
        "uniprot",
        "project_code",
        "donor_code"
    ]
    for col in exclude_columns:
        if context[col] != "all":
            return False
    return True


def get_count_from_cache(context, database_name):
    """
    Get count from cache if possible
    :param context: context dict
    :param database_name: name of db to use e.g. 'immuno'
    :return: dict with status and count
    """
    filter_columns_to_accessor = {
        "mhc_class": "mhc_class",
        "disease": "disease_name",
        "biological_material": "biological_material_name",
        "dignity": "dignity",
        "peptide_length_min": "peptide_length_min",
        "peptide_length_max": "peptide_length_max",
        "include_cell_lines": "is_cell_line",
    }

    query_is_fully_cacheable = get_cacheable_status(context)

    filter_dict = {}
    cols_for_query = ['count']

    # get all columns are filter terms
    for col, accessor in filter_columns_to_accessor.items():
        if col == 'include_cell_lines':
            filter_dict[accessor] = None if context[col] else False
        else:
            filter_dict[accessor] = None if context[col] == "all" else context[col]
        cols_for_query.append(accessor)

    queryset_cache_count = QueryCount.objects.using(database_name).all().values(*cols_for_query).filter(**filter_dict).distinct()

    if len(queryset_cache_count) == 0:
        return {'count': -1, 'status': 'no cache entry'}
    elif len(queryset_cache_count) == 1 and query_is_fully_cacheable:
        return {'count': queryset_cache_count[0].get('count', -1), 'status': 'cache hit'}
    elif len(queryset_cache_count) == 1 and not query_is_fully_cacheable:
        return {'count': queryset_cache_count[0].get('count', -1), 'status': 'partial cache hit'}
    else:
        # if there is more than one result, the cache is ambiguous
        return {'count': -1, 'status': 'no cache entry'}
