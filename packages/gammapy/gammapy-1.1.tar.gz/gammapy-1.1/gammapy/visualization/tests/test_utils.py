# Licensed under a 3-clause BSD style license - see LICENSE.rst
import pytest
import numpy as np
import astropy.units as u
from astropy.table import Table
import matplotlib.pyplot as plt
from gammapy.maps import Map, MapAxis, WcsNDMap
from gammapy.utils.testing import mpl_plot_check, requires_data
from gammapy.visualization import (
    plot_contour_line,
    plot_map_rgb,
    plot_theta_squared_table,
)


def test_map_panel_plotter():
    t = np.linspace(0.0, 6.1, 10)
    x = np.cos(t)
    y = np.sin(t)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    with mpl_plot_check():
        plot_contour_line(ax, x, y)

    x = np.append(x, x[0])
    y = np.append(y, y[0])
    with mpl_plot_check():
        plot_contour_line(ax, x, y)


def test_plot_theta2_distribution():
    table = Table()
    table["theta2_min"] = [0, 0.1]
    table["theta2_max"] = [0.1, 0.2]

    for column in [
        "counts",
        "counts_off",
        "excess",
        "excess_errp",
        "excess_errn",
        "sqrt_ts",
    ]:
        table[column] = [1, 1]

    # open a new figure to avoid
    plt.figure()
    plot_theta_squared_table(table=table)


@requires_data()
def test_plot_map_rgb():
    map_ = Map.read("$GAMMAPY_DATA/cta-1dc-gc/cta-1dc-gc.fits.gz")

    with pytest.raises(ValueError):
        plot_map_rgb(map_)

    with pytest.raises(ValueError):
        plot_map_rgb(map_.sum_over_axes(keepdims=False))

    axis = MapAxis([0, 1, 2, 3], node_type="edges")
    map_allsky = WcsNDMap.create(binsz=10 * u.deg, axes=[axis])
    with mpl_plot_check():
        plot_map_rgb(map_allsky)

    axis_rgb = MapAxis.from_energy_edges(
        [0.1, 0.2, 0.5, 10], unit=u.TeV, name="energy", interp="log"
    )
    map_ = map_.resample_axis(axis_rgb)
    kwargs = {"stretch": 0.5, "Q": 1, "minimum": 0.15}
    with mpl_plot_check():
        plot_map_rgb(map_, **kwargs)
