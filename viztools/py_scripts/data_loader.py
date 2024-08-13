from pygadgetreader import *
import caesar


class DataLoader:

    def __init__(self, snap_file_path, catalog_file_path):
        self.snap_file = snap_file_path
        self.catalog_file = catalog_file_path

    def load_snapshot(self):
        boxsize = readheader(self.snap_file, 'boxsize')
        redshift = readheader(self.snap_file, 'redshift')
        a_scaler = readheader(self.snap_file, 'time')
        h_const = readheader(self.snap_file, 'h')
        gas_pos = readsnap(self.snap_file, 'pos', 'gas') / h_const
        gas_mass = readsnap(self.snap_file, 'mass', 'gas') / h_const
        star_pos = readsnap(self.snap_file, 'pos', 'star') / h_const
        gas_smoothing_lengths = readsnap(self.snap_file, 'hsml', 'gas') / h_const

        return {
            'boxsize': boxsize,
            'redshift': redshift,
            'a_scaler': a_scaler,
            'h_const': h_const,
            'gas_pos': gas_pos,
            'gas_mass': gas_mass,
            'star_pos': star_pos,
            'gas_smoothing_lengths': gas_smoothing_lengths,
        }

    def load_catalog(self):
        obj = caesar.load(self.catalog_file)
        gal_masses = [i.masses['total'] for i in obj.galaxies]
        gal_pos = [gal.pos[:].to('kpccm') for gal in obj.galaxies]
        hi_masses = [gal.masses["HI"] for gal in obj.galaxies]
        i_mass10 = [i for i, mass in enumerate(hi_masses) if mass > 1e10]
        gal_radius = [rad.radii['total_r80'].to('kpccm') for rad in obj.galaxies]

        return {
            'gal_masses': gal_masses,
            'gal_pos': gal_pos,
            'hi_masses': hi_masses,
            'i_mass10': i_mass10,
            'gal_radius': gal_radius,
        }
