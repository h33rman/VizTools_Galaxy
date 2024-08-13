# forms.py

from django import forms

class DataFileForm(forms.Form):
    snap_file_path = forms.CharField(label='Snap File Path', max_length=500)
    catalog_file_path = forms.CharField(label='Catalog File Path', max_length=500)
