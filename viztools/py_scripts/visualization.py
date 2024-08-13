import numpy as np
from . import the_gaussian_kernel
import matplotlib.pyplot as plt


def normalize_visualization(visual2_d):
    max_intensity = np.max(visual2_d)
    if max_intensity > 0:
        visual2_d = visual2_d / max_intensity  # Normalize to the range [0, 1]
    return visual2_d


class Visualizer:
    def __init__(self, gas_data, gas_mass, gas_hsml):
        self.gas_data = gas_data
        self.gas_mass = gas_mass
        self.gas_hsml = gas_hsml
        self.visual2d = None
        self.average_hsml = None

    def compute_simple_gauss(self, visual_size=100):  # default visual_size=100
        visual2d = np.zeros((visual_size, visual_size))
        x_range = [min(self.gas_data[0]), max(self.gas_data[0])]
        y_range = [min(self.gas_data[1]), max(self.gas_data[1])]
        x_width = x_range[1] - x_range[0]
        y_width = y_range[1] - y_range[0]

        scaler = visual_size / max(x_width, y_width)
        gas_hsml_scaled = self.gas_hsml * scaler

        self.average_hsml = np.mean(gas_hsml_scaled)
        pos_i = np.array((self.gas_data[0] - x_range[0]) / x_width * visual_size, dtype=int)
        pos_j = np.array((self.gas_data[1] - y_range[0]) / y_width * visual_size, dtype=int)

        grid_x, grid_y = the_gaussian_kernel.create_grid(_size=visual_size)

        for i in range(len(pos_i)):
            visual2d += self.gas_mass[i] * the_gaussian_kernel.gaussian_kernel(
                pos_i[i], pos_j[i], gas_hsml_scaled[i], self.gas_mass[i], grid_x, grid_y)

        self.visual2d = visual2d

    def plot_visual(self, x_range, y_range):
        if self.visual2d is None:
            raise ValueError("No visualization computed! Use 'compute_simple_gauss' method first.")

        plt.figure(figsize=(10, 10))
        plt.imshow(self.visual2d.T, origin='lower', cmap='viridis',
                   extent=[x_range[0], x_range[1], y_range[0], y_range[1]])
        plt.title('Galaxy Visualization')
        plt.xlabel('X axis (kpc)')
        plt.ylabel('Y axis (kpc)')
        plt.colorbar(label='Intensity')
        #plt.show()

        # Save the plot
        image_path= 'static/galaxy_visualization.png'
        plt.savefig(image_path)

        return image_path
