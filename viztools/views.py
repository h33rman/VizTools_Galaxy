from django.shortcuts import render, redirect
from .forms import DataFileForm
from .py_scripts import data_loader, galaxy_selection, visualization


def upload_file(request):
    if request.method == 'POST':
        form = DataFileForm(request.POST)
        if form.is_valid():
            snap_file_path = form.cleaned_data['snap_file_path']
            catalog_file_path = form.cleaned_data['catalog_file_path']

            # Store paths in session to use them in other views
            request.session['snap_file_path'] = snap_file_path
            request.session['catalog_file_path'] = catalog_file_path

            return redirect('select_galaxy')
    else:
        form = DataFileForm()
    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')


def select_galaxy(request):
    snap_file_path = request.session.get('snap_file_path')
    catalog_file_path = request.session.get('catalog_file_path')

    if not snap_file_path or not catalog_file_path:
        return redirect('upload')  # Redirect to upload if paths are missing

    loader = data_loader.DataLoader(snap_file_path, catalog_file_path)
    snapshot_data = loader.load_snapshot()
    catalog_data = loader.load_catalog()

    # Initialize GalaxySelector
    galaxy_selector = galaxy_selection.GalaxySelector({**snapshot_data, **catalog_data})

    if request.method == 'POST':
        galaxy_index = int(request.POST['galaxy_index'])

        # Select galaxy
        galaxy_selector.select_galaxy(i_pos=galaxy_index)
        gas_x, gas_y, gas_z = galaxy_selector.particles_within()


def visualize_galaxy(request):
    snap_file_path = request.session.get('snap_file_path')
    catalog_file_path = request.session.get('catalog_file_path')

    if not snap_file_path or not catalog_file_path:
        return redirect('upload')  # Redirect to upload if paths are missing

    loader = data_loader.DataLoader(snap_file_path, catalog_file_path)
    snapshot_data = loader.load_snapshot()
    catalog_data = loader.load_catalog()

    # Initialize GalaxySelector
    galaxy_selector = galaxy_selection.GalaxySelector({**snapshot_data, **catalog_data})

    if request.method == 'POST':
        galaxy_index = int(request.POST['galaxy_index'])

        # Select galaxy
        galaxy_selector.select_galaxy(i_pos=galaxy_index)
        gas_x, gas_y, gas_z = galaxy_selector.particles_within()

        # Visualize galaxy
        visualizer = visualization.Visualizer(
            gas_data=(gas_x, gas_y),
            gas_mass=snapshot_data['gas_mass'][galaxy_selector.selected_index],
            gas_hsml=snapshot_data['gas_smoothing_lengths'][galaxy_selector.selected_index]
        )
        choose_visual = int(request.POST['choose_visual'])

        visualizer.compute_simple_gauss(visual_size=choose_visual)
        visualizer.plot_visual(x_range=[min(gas_x), max(gas_x)], y_range=[min(gas_y), max(gas_y)])


    return render(request, 'visualize_galaxy.html')