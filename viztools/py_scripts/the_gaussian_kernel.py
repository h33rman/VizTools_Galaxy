import numpy as np
# Create Grid
def create_grid(_size):
    """
    Create a 2D grid of size _size x _size.
    """
    _x, _y = np.mgrid[0:_size, 0:_size]
    return _x, _y


def gaussian_kernel(x, y, _sigma, _mass, grid_x=None, grid_y=None):
    """
    Create a 2D Gaussian kernel with the given parameters.
    :param x: X-coordinate of the Gaussian center.
    :param y: Y-coordinate of the Gaussian center.
    :param _sigma: Standard deviation of the Gaussian kernel.
    :param _mass: Mass of the Gaussian kernel.
    :param grid_x: X-coordinates of the grid.
    :param grid_y: Y-coordinates of the grid.
    """

    gauss_k = (
        np.exp(-((grid_x - x) ** 2 + (grid_y - y) ** 2) / (2 * _sigma**2))
        * _mass
        / (2 * np.pi * _sigma**2)
    )
    return gauss_k
