from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, Reset
from crispy_forms.helper import FormHelper


class ShowMoreForm(forms.Form):
    show_more_sample_infos = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit();'}))
    show_more_donor_infos = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit();'}))


class PSMFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        'status',
        Submit('submit', 'Apply Filter'),
    )


class DownloadQueryForm(forms.Form):
    sequence = forms.TextInput()
    mhc_class = forms.TextInput()
    modifications = forms.TextInput()
    uniprot = forms.TextInput()
    disease = forms.TextInput()
    biological_material = forms.TextInput()
    dignity = forms.TextInput()


class DownloadForm(forms.Form):
    pass
