import logging
import typing as t
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django_filters.views import FilterView
from django_tables2 import LazyPaginator, SingleTableMixin,RequestConfig
from django_tables2.export.views import ExportMixin
from django.utils.decorators import method_decorator
from typing import Any, Dict, Optional

from .filters import PeptideSpectrumMatchesMatViewFilter
from .forms import ShowMoreForm
from .models import *
from .tables import PSMSTable
from .utils.io import csv_output, xslx_output
from .utils.plot_spectrum import make_plot
from .utils.queryset_utils import generate_filtered_query, get_queryset_count, append_context_for_dl
from .utils.db_mapping import map_db_name


# type alias when response is one of these types
RedirectOrResponse = t.Union[HttpResponseRedirect, HttpResponse]

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("DB Query")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


def home(request) -> HttpResponse:
    return render(request, 'query/home.html')


def overview(request) -> HttpResponse:
    return render(request, 'query/overview.html')


def legal_notice(request) -> HttpResponse:
    return render(request, 'query/legal_notice.html')


def privacy_policy(request) -> HttpResponse:
    return render(request, 'query/privacy_policy.html')


def signupuser(request) -> RedirectOrResponse:
    if request.method == 'GET':
        return render(request, 'query/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.is_active = False
                user.save()
                login(request, user)
                messages.info(request, 'Thank you for your registration. Our team will activate your account shortly.')
                return redirect('psms')
            except IntegrityError:
                return render(request, 'query/signupuser.html', {'form': UserCreationForm(),
                                                                 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'query/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'query/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'query/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('psms')


@login_required
def logoutuser(request) -> HttpResponseRedirect:
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class PSMView(ExportMixin, SingleTableMixin, FilterView):
    """
    Generates main table and filters of the PCI-DB
    """
    model = PeptideSpectrumMatchesMatView
    table_class = PSMSTable
    template_name = 'query/psms.html'
    paginator_class = LazyPaginator

    filterset_class = PeptideSpectrumMatchesMatViewFilter

    def get_queryset(self) -> Any:
        database_name = map_db_name(self.request.GET.get('database', 'immuno'))
        queryset = super().get_queryset().using(database_name)
        
        # manually remove HNSSC1 samples
        queryset = queryset.exclude(ms_run_code__sample_code__donor_code__donor_code__startswith='HNSCC1')
        
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['show_more_form'] = ShowMoreForm(self.request.GET)

        database_name = map_db_name(self.request.GET.get('database', 'immuno'))
        queryset = generate_filtered_query(self.request, database_name)
        query_context = append_context_for_dl(self.request, context)
        queryset = queryset.exclude(ms_run_code__sample_code__donor_code__donor_code__startswith='HNSCC1')  # manually remove HNSSC1 samples

        # number_of_rows_output = get_queryset_count(queryset, query_context, database=database_name)
        context['query_count'] = ""
        return context

    def get_table(self, **kwargs: Any) -> PSMSTable:
        """
        Return a table object to use. The table has automatic support for
        sorting and pagination.
        """
        hide_ms_info = ['filename', 'dignity', 'is_metastasis', 'is_cell_line', 'treatment', 'donor_code', 'donor_hla_types', 'project_code']

        # Handle the form submission and get the form data
        show_more_form = ShowMoreForm(self.request.GET)
        if show_more_form.is_valid():
            show_more_sample_infos = show_more_form.cleaned_data['show_more_sample_infos']
            show_more_donor_infos = show_more_form.cleaned_data['show_more_donor_infos']

            if show_more_sample_infos:  # sample infos
                hide_ms_info.remove('dignity')
                hide_ms_info.remove('is_metastasis')
                hide_ms_info.remove('is_cell_line')
                hide_ms_info.remove('treatment')

            if show_more_donor_infos:  # remove donor infos
                hide_ms_info.remove('donor_code')
                hide_ms_info.remove('donor_hla_types')
                hide_ms_info.remove('project_code')

        table = PSMSTable(data=self.get_table_data(), exclude=hide_ms_info)
        return RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(
            table
        )

    def get_table_data(self) -> Any:
        data = super().get_table_data()
        if '_export' in self.request.GET:  # when exporting, show 10000 rows
            max_rows = 100
            dataset = data[:max_rows]
            return dataset

        else:
            return data

@login_required
def psm_spectrum_info(request: HttpRequest, psm_code: int) -> HttpResponse:
    """
    Visualization of the spectra.
    """
    database_name: str = map_db_name(request.GET.get('database', 'immuno'))

    psm = get_object_or_404(
        PeptideSpectrumMatchesMatView.objects.using(database_name), 
        pk=psm_code
    )
    spectrum = get_object_or_404(
        Spectra.objects.using(database_name), 
        pk=psm_code
    )
    spectrum_path: str = spectrum.spectrum

    plot_data: str = make_plot(
        psm.peptide_sequence,
        spectrum_path,
        False
    )

    mass_spectrometer_name: str = psm.ms_run_code.mass_spectrometer_code.mass_spectrometer_name

    # Context to render
    context: Dict[str, Any] = {
        'psm': psm,
        'database_name': database_name,
        'mass_spectrometer_name': mass_spectrometer_name,
        'graphic': plot_data,
    }
    return render(request, 'query/psm_spectrum_info.html', context)



