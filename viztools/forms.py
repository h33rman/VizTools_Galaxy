from django import forms

class FileSelectionForm(forms.Form):
    snap_file = forms.CharField(label='Snapshot File Path', max_length=255)
    catalog_file = forms.CharField(label='Catalog File Path', max_length=255)

class GalaxySelectionForm(forms.Form):
    galaxy_index = forms.IntegerField(label='Galaxy Index')
    visualization_size = forms.IntegerField(label='Visualization Size', required=False)
