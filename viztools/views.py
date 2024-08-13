from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DataFileForm
from .py_scripts import data_loader

def upload_file(request):
    if request.method == 'POST':
        form = DataFileForm(request.POST)
        if form.is_valid():
            # Save the file paths
            snap_file_path = form.cleaned_data['snap_file_path']
            catalog_file_path = form.cleaned_data['catalog_file_path']

            # You can now pass these paths to your DataLoader or other modules
            # Example:
            loader = data_loader.DataLoader(snap_file_path, catalog_file_path)
            snapshot_data = loader.load_snapshot()
            catalog_data = loader.load_catalog()

            return redirect('upload_success')
    else:
        form = DataFileForm()
    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return HttpResponse("Files were successfully linked.")
