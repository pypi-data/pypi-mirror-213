""" Module testing mesh ID card generation """
from collections import namedtuple
import os
import numpy as np
from reportlab.lib.pagesizes import A4
import h5py
from pyhip.commands.mesh_idcard import (_get_datasets,
                                        extract_hdf_meshinfo,
                                        arrange_meshinfo,
                                        _create_perspective_mark,
                                        _get_boundary_nodes,
                                        plot_2d_density_view,
                                        plot_3d_density_view,
                                        _get_plot_size,
                                        generate_mesh_idcard)

Bounds = namedtuple('Bounds', ['min', 'max'])
LANDSCAPE = (960., 480.)

def test_get_datasets(datadir):
    """ test of extraction of datasets from hdf file """
    meshfile = datadir.join('trapped_vtx.mesh.h5')
    ds_name = ['volume', 'PatchLabels']
    with h5py.File(meshfile, 'r') as fin:
        data_dict = _get_datasets(fin, ds_name)

    assert list(data_dict.keys()) == ['PatchLabels', 'volume']
    assert data_dict['PatchLabels'].shape == (15,)
    assert data_dict['volume'].shape == (34684,)

    gr_skip = ['Boundary']
    with h5py.File(meshfile, 'r') as fin:
        data_dict = _get_datasets(fin, ds_name, gr_skip=gr_skip)
    assert list(data_dict.keys()) == ['volume']

def test_extract_hdf_meshinfo(datadir):
    """ test extraction of mesh info from hdf mesh file """
    meshfile = datadir.join('trapped_vtx.mesh.h5')
    meshinfo_dict, is_axi, ndim, _ = extract_hdf_meshinfo(str(meshfile))
    meshinfo_exp = {'Mesh name': 'trapped_vtx.mesh.h5',
                    'Hip version': "20.03.1 'Rhytidiadelphus squarrosus'",
                    'Number of nodes': 34684,
                    'Number of boundary nodes': 9436,
                    'Domain volume [m3]': 0.0004794414903089477,
                    'Number of cells': {'Tetrahedra': 177563},
                    'Metric': {'Edge length [m]': Bounds(min=0.0010846189782710055,
                                                         max=0.006078197620620785),
                               'Element volume [m3]': Bounds(min=6.466297253616193e-10,
                                                             max=7.251232840984067e-09)},
                    'Bounding box': {'x [m]': Bounds(min=0.0,
                                                     max=0.2),
                                     'r [m]': Bounds(min=0.07998170722231683,
                                                     max=0.130384048104053),
                                     'theta [deg]': Bounds(min=-20.00000049987848,
                                                           max=20.00000081092912)},
                    'Periodic angle\xa0[deg]': -40.0,
                    'Periodic pairs': {'': 'PerioRight - PerioLeft'}}
    assert meshinfo_dict == meshinfo_exp
    assert is_axi == True
    assert ndim == 3

    meshfile = datadir.join('maveric_coarse.mesh.h5')
    meshinfo_dict, is_axi, ndim, _ = extract_hdf_meshinfo(str(meshfile))

    meshinfo_exp = {'Mesh name': 'maveric_coarse.mesh.h5',
                    'Hip version': "19.12.0 'Rhytidiadelphus squarrosus'",
                    'Number of nodes': 36000,
                    'Number of boundary nodes': 12320,
                    'Domain volume [m3]': 2.364542976007393e-06,
                    'Number of cells': {'Tetrahedra': 180576},
                    'Metric': {'Edge length [m]': Bounds(min=0.00033699999999943194,
                                                         max=0.000762733812429156),
                               'Element volume [m3]': Bounds(min=1.3094447634214457e-11,
                                                             max=1.3094447634237618e-11)},
                    'Bounding box': {'x [m]': Bounds(min=0.0,
                                                     max=0.04568000000000001),
                                     'y [m]': Bounds(min=-0.0104,
                                                     max=0.0096),
                                     'z [m]': Bounds(min=-0.0013479999999997199,
                                                     max=0.001348)},
                    'Periodic pairs': {'': 'Wall_right_injection - Wall_left_injection',
                                       ' ': 'Wall_right_suction - Wall_left_suction'}}
    assert meshinfo_dict == meshinfo_exp
    assert is_axi == False
    assert ndim == 3

def test_arrange_meshinfo(datadir):
    """ test formatting of meshinfo into lines """
    meshfile = datadir.join('maveric_coarse.mesh.h5')
    meshinfo_dict, _, _, _ = extract_hdf_meshinfo(str(meshfile))
    lines = arrange_meshinfo(meshinfo_dict)

    lines_exp = [
        "Mesh name                  maveric_coarse.mesh.h5",
        "Hip version                19.12.0 'Rhytidiadelphus squarrosus'",
        "Number of nodes            36'000",
        "Number of boundary nodes   12'320",
        "Domain volume [m3]         2.364543e-06",
        "Number of cells            ",
        "  Tetrahedra               180'576",
        "Metric                     ",
        "  Edge length [m]          min=0.000337          max=0.000763",
        "  Element volume [m3]      min=1.309445e-11      max=1.309445e-11",
        "Bounding box               ",
        "  x [m]                    min=0.000000e+00      max=4.568000e-02",
        "  y [m]                    min=-0.010400         max=0.009600",
        "  z [m]                    min=-0.001348         max=0.001348",
        "Periodic pairs             ",
        "                           Wall_right_injection - Wall_left_injection",
        "                           Wall_right_suction - Wall_left_suction"]
    assert lines == lines_exp

def test_create_perspective_mark():
    """ test of creation of perspective mark xyz array """

    xyz_arr = np.array([[-1., +1., -1.],
                        [-1., +1., +1.],
                        [-1., -1., +1.],
                        [-1., -1., -1.],
                        [+0., +1., -1.],
                        [+0., +1., +1.],
                        [+0., -1., +1.],
                        [+0., -1., -1.],
                        [+1., +1., -1.],
                        [+1., +1., +1.],
                        [+1., -1., +1.],
                        [+1., -1., -1.]])
    xyz_perspec = _create_perspective_mark(
        xyz_arr,
        ([1, 0, 0], 90.),
        ([0., 2.5, 4.7], 12.1),
        coef=2.)

    xyz_exp = [[-2.52257855, +1.77489909, +1.57681029],
               [-2.12882016, -2.20550250, +1.61365531],
               [-1.38855440, -2.16865748, -2.31707605],
               [-1.78231278, +1.81174411, -2.35392107],
               [-0.28350604, +0.98588914, +0.97347159],
               [-0.08662684, -1.00431165, +0.99189410],
               [+0.28350604, -0.98588914, -0.97347159],
               [+0.08662684, +1.00431165, -0.99189410],
               [+0.34713860, +0.54216437, +0.57926901],
               [+0.44557820, -0.45293603, +0.58848027],
               [+0.63064464, -0.44372477, -0.39420257],
               [+0.53220504, +0.55137562, -0.40341383]]
    np.testing.assert_allclose(xyz_perspec, xyz_exp)

def test_get_boundary_nodes(datadir):
    """ test of extraction of nodes on boundaries from meshfile """
    meshfile = datadir.join('maveric_coarse.mesh.h5')
    x_arr, y_arr, z_arr = _get_boundary_nodes(meshfile, 3)

    assert x_arr.shape == (12320,)
    assert y_arr.shape == (12320,)
    assert z_arr.shape == (12320,)

def test_plot_density_view(datadir):
    """ test the plot of density views """
    meshfile = datadir.join('maveric_coarse.mesh.h5')
    buffer_ = plot_3d_density_view(meshfile, 'cart')
    assert bool(buffer_.getvalue())

    meshfile = datadir.join('trapped_vtx.mesh.h5')
    buffer_ = plot_3d_density_view(meshfile, 'axicyl')
    assert bool(buffer_.getvalue())

def test_get_plot_size():
    """ test of the computation of fig size """
    width, height = _get_plot_size(10., 5., 15., 2.)

    np.testing.assert_allclose(width, 9.9)
    np.testing.assert_allclose(height, 1.32)

def test_generate_mesh_idcard(datadir):
    """ functionnal test of generate_mesh_idcard """

    meshfile = datadir.join('trapped_vtx.mesh.h5')

    generate_mesh_idcard(str(meshfile), A4)
    assert os.path.isfile('./trapped_vtx.mesh.pdf')
    os.remove('./trapped_vtx.mesh.pdf')

    generate_mesh_idcard(str(meshfile), LANDSCAPE)
    assert os.path.isfile('./trapped_vtx.mesh.pdf')
    os.remove('./trapped_vtx.mesh.pdf')
