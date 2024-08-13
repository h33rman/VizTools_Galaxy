import numpy as np


class GalaxySelector:
    def __init__(self, data):
        self.data = data
        self.selected_galaxy = None
        self.selected_radius = None
        self.selected_index = None

    def select_galaxy(self, i_pos):
        if i_pos < len(self.data['gal_pos']):
            self.selected_galaxy = self.data['gal_pos'][i_pos].value
            self.selected_radius = self.data['gal_radius'][i_pos].value / self.data['a_scaler']
            print(f"Selected Galaxy Radius: {self.selected_radius}")

            return self.selected_galaxy, self.selected_radius
        else:
            raise ValueError(f"Galaxy index {i_pos} is out of range!")

    def particles_within(self):
        if self.selected_galaxy is None or self.selected_radius is None:
            raise ValueError("No galaxy selected! Use 'select_galaxy' method first.")

        distances_squared = ((self.data['gas_pos'][:, 0] - self.selected_galaxy[0]) ** 2 +
                             (self.data['gas_pos'][:, 1] - self.selected_galaxy[1]) ** 2 +
                             (self.data['gas_pos'][:, 2] - self.selected_galaxy[2]) ** 2)
        self.selected_index = np.where(distances_squared < self.selected_radius ** 2)
        within_radius = self.data['gas_pos'][self.selected_index]
        gas_select_x = within_radius[:, 0]
        gas_select_y = within_radius[:, 1]
        gas_select_z = within_radius[:, 2]

        return gas_select_x, gas_select_y, gas_select_z
