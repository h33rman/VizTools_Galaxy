from django.shortcuts import render
from .forms import FileSelectionForm, GalaxySelectionForm
from .py_scripts import data_loader, galaxy_selection, visualization
from django.http import HttpResponseRedirect
from django.urls import reverse


def upload_file(request):
    if request.method == 'POST':
        form = FileSelectionForm(request.POST)
        if form.is_valid():
            # Save the file paths to the session
            request.session['snap_file'] = form.cleaned_data['snap_file']
            request.session['catalog_file'] = form.cleaned_data['catalog_file']
            return HttpResponseRedirect(reverse('select_galaxy'))
    else:
        form = FileSelectionForm()
    return render(request, 'viztools/upload_file.html', {'form': form})

def select_galaxy(request):
    if request.method == 'POST':
        form = GalaxySelectionForm(request.POST)
        if form.is_valid():
            request.session['galaxy_index'] = form.cleaned_data['galaxy_index']
            request.session['visualization_size'] = form.cleaned_data['visualization_size'] or 100
            return HttpResponseRedirect(reverse('visualization_result'))
    else:
        form = GalaxySelectionForm()
    return render(request, 'viztools/select_galaxy.html', {'form': form})

def visualization_result(request):
    snap_file = request.session.get('snap_file')
    catalog_file = request.session.get('catalog_file')
    galaxy_index = request.session.get('galaxy_index')
    visualization_size = request.session.get('visualization_size')

    loader = data_loader.DataLoader(snap_file, catalog_file)
    snapshot_data = loader.load_snapshot()
    catalog_data = loader.load_catalog()

    combined_data = {**snapshot_data, **catalog_data}

    selector = galaxy_selection.GalaxySelector(combined_data)
    selector.select_galaxy(i_pos=galaxy_index)
    gas_x, gas_y, gas_z = selector.particles_within()

    visualizer = visualization.Visualizer(
        gas_data=(gas_x, gas_y, gas_z),
        gas_mass=snapshot_data['gas_mass'][selector.selected_index],
        gas_hsml=snapshot_data['gas_smoothing_lengths'][selector.selected_index]
    )

    visualizer.compute_simple_gauss(visual_size=visualization_size)
    x_range = [min(gas_x), max(gas_x)]
    y_range = [min(gas_y), max(gas_y)]
    image_path = visualizer.plot_visual(x_range, y_range)

    return render(request, 'viztools/visualization_result.html', {'image_path': image_path})
