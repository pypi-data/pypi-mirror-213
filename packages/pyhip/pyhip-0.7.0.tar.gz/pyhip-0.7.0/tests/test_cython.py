""" tests for Cython version of hip commands"""
import os
import pytest
from pyhip.commands.readers import (read_mesh_files,
                                    read_ensight_mesh,
                                    read_gmsh_mesh,
                                    read_cgns_mesh,
                                    read_hdf5_mesh,
                                    read_fluent_mesh,
                                    read_centaur_mesh)
from pyhip.commands.writers import (_write_file,
                                    write_avbp,
                                    write_fieldview,
                                    write_gmsh,
                                    write_ensight,
                                    write_cgns,
                                    write_hdf5,
                                    dump_wired)
from pyhip.commands.operations import (_generate_2d_mesh,
                                       _extrude_2d_mesh,
                                       _convert_quad2tri,
                                       _convert_hex2tet,
                                       generate_mesh_2d_3d,
                                       adapt_with_factor,
                                       adapt_with_var,
                                       interpolate,
                                       transform_translate,
                                       transform_rotate,
                                       transform_scale,
                                       duplicate,
                                       transform_reflect,
                                       set_bctype,
                                       set_bctext,
                                       list_periodic,
                                       list_surface,
                                       set_checklevel,
                                       hip_exit)


#functional tests of the various commands, first up is hip_exit
# def test_exit():
#     """test for exit function in fallback"""
#     tgt = ["exit"]

#     _, cmd = hip_exit(fallback=False)
#     assert cmd == tgt

# # readers commands tests
# def test_read_hdf5(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "read hdf5 %s" % 'trappedvtx.mesh.h5',
#             "var"]

#     cmds = read_hdf5_mesh(file, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# def test_read_fluent(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('default_id.msh')
#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "read fluent %s" % 'default_id.msh',
#             "var"]

#     cmds = read_fluent_mesh(file, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# # @pytest.mark.skip(reason="SIGABRT 6, apparent hdf5 libraries version mismatch")
# def test_read_cgns(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.grid.cgns')
#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "read cgns %s" % 'trappedvtx.grid.cgns',
#             "var"]

#     cmds = read_cgns_mesh(file, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# # @pytest.mark.skip(reason="SIGSEGV 11, error reading ensight mesh")
# def test_read_ensight(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.case')
#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "read ensight %s" % 'trappedvtx.case',
#             "var"]

#     cmds = read_ensight_mesh(file, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# def test_read_gmsh(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.msh')

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "read gmsh trappedvtx.msh",
#             "var"]
#     cmds = read_gmsh_mesh(file, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# @pytest.mark.skip(reason="missing meshfile for the test")
# def test_read_centaur(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('')

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "read centaur %s" % '',
#             "var"]
#     cmds = read_centaur_mesh(file, fallback=False)
#     assert cmds == tgts

#     _, _ = hip_exit(fallback=False)

# # writer commands tests
# def test_write_hdf5(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "write hdf5 -a new"]

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# def test_write_cgns(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "write cgns new"]

#     fout = datadir.join('new')
#     cmds = write_cgns(fout, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# def test_write_ensight(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "write ensight -3 new"]

#     fout = datadir.join('new')
#     cmds = write_ensight(fout, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# def test_write_fieldview(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "write fieldview new"]

#     fout = datadir.join('new')
#     cmds = write_fieldview(fout, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# def test_write_gmsh(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "write gmsh new"]

#     fout = datadir.join('new')
#     cmds = write_gmsh(fout, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# def test_write_avbp(datadir):
#     """functional test for meshfiles reader"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
#             "write avbp new"]

#     fout = datadir.join('new')
#     cmds = write_avbp(fout, fallback=False)

#     assert cmds == tgts
#     _, _ = hip_exit(fallback=False)

# #functional tests of operation methods
# @pytest.mark.skip(reason="missing metric content")
# def test_adapt_with_var(datadir):
#     """missing metric content"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     fout = datadir.join('new')
#     cmds = write_avbp(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_adapt_with_factor(datadir):
#     """missing metric content"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["mmg3d -f 1.0"]
#     cmd = adapt_with_factor(1.)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_set_bc(datadir):
#     """test on bc contents"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["set bc-text Inlet inlet"]
#     cmd = set_bctext('Inlet', 'inlet', fallback=False)
#     assert cmd == tgt

#     tgt = ['set bc-type inlet n']
#     cmd = set_bctype('inlet', 'n', fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_set_checklevel(datadir):
#     """test on bc contents"""
#     tgt = ["set checklevel 0"]
#     cmd = set_checklevel(0, fallback=False)
#     assert cmd == tgt

#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     tgt = ["set checklevel 1"]
#     cmd = set_checklevel(1, fallback=False)
#     assert cmd == tgt

#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     tgt = ["set checklevel 2"]
#     cmd = set_checklevel(2, fallback=False)
#     assert cmd == tgt

#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     tgt = ["set checklevel 3"]
#     cmd = set_checklevel(3, fallback=False)
#     assert cmd == tgt

#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     tgt = ["set checklevel 4"]
#     cmd = set_checklevel(4, fallback=False)
#     assert cmd == tgt

#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     tgt = ["set checklevel 5"]
#     cmd = set_checklevel(5, fallback=False)
#     assert cmd == tgt

#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     with pytest.raises(TypeError):
#         assert set_checklevel(4.5, fallback=False)
#         assert set_checklevel([3], fallback=False)
#     with pytest.raises(ValueError):
#         assert set_checklevel(6, fallback=False)
#         assert set_checklevel(-1, fallback=False)

# def test_interpolate(datadir):
#     """test on interpolation"""
#     file = datadir.join('default.mesh.h5')
#     sol = datadir.join('default_inst.sol.h5')
#     _ = read_hdf5_mesh(file, fallback=False, sol_file=sol)
#     _ = set_bctext('Inlet', 'inlet', fallback=False)
#     _ = set_bctext('Outlet', 'outlet', fallback=False)
#     _ = set_bctext('PerioLeft', 'perioleft', fallback=False)
#     _ = set_bctext('PerioRight', 'perioright', fallback=False)
#     _ = set_bctext('WallIn1', 'wallin1', fallback=False)
#     _ = set_bctext('WallIn2', 'wallin2', fallback=False)
#     _ = set_bctext('WallIn3', 'wallin3', fallback=False)
#     _ = set_bctext('MultiperfIn', 'multiperfin', fallback=False)
#     _ = set_bctext('WallIn4', 'wallin4', fallback=False)
#     _ = set_bctext('InletHole', 'inlethole', fallback=False)
#     _ = set_bctext('WallOut', 'wallout', fallback=False)
#     _ = set_bctext('CanyonUp', 'canyonup', fallback=False)
#     _ = set_bctext('CanyonBottom', 'canyonbottom', fallback=False)
#     _ = set_bctext('CanyonDown', 'canyondown', fallback=False)
#     _ = set_bctext('InletFilm', 'inletfilm', fallback=False)

#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["interpolate grid 1"]
#     cmd = interpolate(fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_transform_translate(datadir):
#     """test on transform contents"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["transform translate 1 0 0"]
#     cmd = transform_translate(1,0,0, fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_transform_scale(datadir):
#     """test on transform contents"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["transform scale 1 0.5 0.5"]
#     cmd = transform_scale(1,0.5,0.5, fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_transform_reflect(datadir):
#     """test on transform contents"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["transform reflect x"]
#     cmd = transform_reflect('x', fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)
    
#     with pytest.raises(ValueError):
#         assert transform_reflect('w', fallback=False)

# def test_transform_rotate(datadir):
#     """test on transform contents"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["transform rotate x 45"]
#     cmd = transform_rotate('x', 45, fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     with pytest.raises(ValueError):
#         assert transform_rotate('w', 45, fallback=False)

# def test_duplicate(datadir):
#     """test on transform contents"""
#     file = datadir.join('trappedvtx.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["copy uns 2 rotate x 40.0"]
#     cmd = duplicate(2, 40.0, fallback=False)
#     assert cmd == tgt

#     tgt = ["copy uns 2 translate  0.2 0 0"]
#     cmd = duplicate(2, [0.2, 0, 0], operation='translate', fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     with pytest.raises(ValueError):
#         assert duplicate('w', 45.0, fallback=False)
#         assert duplicate(2, 45, fallback=False)
#         assert duplicate(2, 45.0, axis='w', fallback=False)
#         assert duplicate(2, 45.0, operation='none', fallback=False)
#         assert duplicate(2, 45.0, operation='translate', fallback=False)
#         assert duplicate(2, [45.0, 20], operation='translate', fallback=False)

# def test_generate(datadir):
#     """generation and extrusion test"""
#     tgt = ["generate 0 0 1 1 6 6"]
#     cmd = _generate_2d_mesh([0, 0], [1, 1], [6, 6], fallback=False)
#     assert cmd == tgt

#     tgt = ["copy 3D 0 1 6 z"]
#     cmd = _extrude_2d_mesh([0, 1], 6, 'z', fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     tgt = ["generate 0 0 1 1 6 6"]
#     cmd = _generate_2d_mesh([0, 0], [1, 1], [6, 6], fallback=False)
#     assert cmd == tgt

#     tgt = ["copy 3D 0 40 6 axi"]
#     cmd = _extrude_2d_mesh([0, 40], 6, 'axi', fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     tgt = ["generate 0 0 1 1 6 6"]
#     cmd = _generate_2d_mesh([0, 0], [1, 1], [6, 6], fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     with pytest.raises(ValueError):
#         assert _generate_2d_mesh([1, 1], [0, 0], [5, 5], fallback=False)
#         assert _extrude_2d_mesh([0, 1], 6, 'w', fallback=False)
#         assert _extrude_2d_mesh([1, 0], 6, 'x', fallback=False)

# def test_convert_q2t(datadir):
#     """conversion to tri test"""
#     _ = _generate_2d_mesh([0, 0], [1, 1], [6, 6], fallback=False)

#     tgt = ["copy q2t"]
#     cmd = _convert_quad2tri(fallback=False)
#     assert cmd == tgt

#     cmd = _extrude_2d_mesh([0, 1], 6, 'x', fallback=False)

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     _ = _generate_2d_mesh([0, 0], [1, 1], [6, 6], fallback=False)

#     tgt = ["copy q2t"]
#     cmd = _convert_quad2tri(fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_convert_2tets(datadir):
#     """conversion to tet test"""
#     _ = _generate_2d_mesh([0, 0], [1, 1], [6, 6], fallback=False)

#     cmd = _extrude_2d_mesh([0, 1], 6, 'x', fallback=False)

#     tgt = ["copy 2tets"]
#     cmd = _convert_hex2tet(fallback=False)
#     assert cmd == tgt

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

# def test_generate_mesh_2d_3d(datadir):
#     """full generation with conversions"""
#     tgts = ["generate 0 0 1 1 6 6",
#             "copy 3D 0 1 6 z"]
#     cmds = generate_mesh_2d_3d((0, 0, 0), (1, 1, 1), (6, 6, 6), 'z', fallback=False)
#     assert tgts == cmds

#     fout = datadir.join('new')
#     cmds = write_hdf5(fout, fallback=False)

#     _, _ = hip_exit(fallback=False)

#     with pytest.raises(TypeError):
#         assert generate_mesh_2d_3d((0, 0, 0), (1, 1, 1), {6, 6, 6}, 'z', fallback=False)
#     with pytest.raises(ValueError):
#         assert generate_mesh_2d_3d((0, 0, 0), (1, 1, 1), (6, 6), 'z', fallback=False)
#         assert generate_mesh_2d_3d((0, 0, 0), (1, 1, 1), (6, 6, ), 'z', fallback=False)
#         assert generate_mesh_2d_3d((0, 0, 0, 0), (1, 1, 1, 1), (6, 6, 6, 6), 'z', fallback=False)
#         assert generate_mesh_2d_3d([0], [1], [6], 'z', fallback=False)

# def test_list(datadir):
#     """lists trivial testing"""
#     file = datadir.join('new.mesh.h5')
#     _ = read_hdf5_mesh(file, fallback=False)

#     tgt = ["list surface"]
#     cmd = list_surface(fallback=False)
#     assert cmd == tgt

#     tgt = ["list periodic"]
#     cmd = list_periodic(fallback=False)
#     assert cmd == tgt

#     _, _ = hip_exit(fallback=False)
