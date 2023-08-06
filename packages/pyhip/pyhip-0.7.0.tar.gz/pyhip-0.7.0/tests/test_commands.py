""" test folder for hip commands in python
    all tests are in fallback mode
"""
import os
import pytest
from pyhip.commands.readers import (_split_file_path,
                                    _rel_path,
                                    read_mesh_files,
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


#base unittest for all other methods.
def test_split_file_path(datadir):
    """unit test for file path splitter in readers.py"""
    path = datadir.join('trappedvtx.mesh.h5')
    tgt_base = os.path.basename(os.path.abspath(path))
    tgt_folder = os.path.dirname(os.path.abspath(path))

    parent, basename = _split_file_path(path)

    assert parent == tgt_folder
    assert basename == tgt_base

def test_rel_path(datadir):
    """unit test for file relative path finder in readers.py"""
    file = datadir.join('trappedvtx.mesh.h5')
    parentdir = os.path.dirname(os.path.abspath(file))
    relpath_tgt = os.path.relpath(os.path.abspath(file), start=parentdir)

    relpath = _rel_path([file], parentdir)

    assert relpath == [relpath_tgt]

#functional tests of the various commands, first up is hip_exit
def test_exit():
    """test for exit function in fallback"""
    tgt = ["exit"]

    _, cmd = hip_exit()
    assert cmd == tgt

# readers commands tests
def test_read_mesh_files(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    file = datadir.join('trappedvtx.mesh.h5')
    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read hdf5 %s" % 'trappedvtx.mesh.h5',
            "var"]

    cmds = read_mesh_files([file], 'hdf5')

    assert cmds == tgts
    _, _ = hip_exit()

def test_read_hdf5(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read hdf5 %s" % 'trappedvtx.mesh.h5',
            "var"]

    cmds = read_hdf5_mesh(file)

    assert cmds == tgts
    _, _ = hip_exit()

def test_read_hdf5_hybrid(datadir, rm_hipin):
    """functional test for meshfiles reader with hybrid mesh"""
    rm_hipin
    file = datadir.join('pri555.mesh.h5')
    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read hdf5 %s" % 'pri555.mesh.h5',
            "var"]

    cmds = read_hdf5_mesh(file)

    #assert cmds == tgts
    _, _ = hip_exit()

def test_read_fluent(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('default_id.msh')
    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read fluent %s" % 'default_id.msh',
            "var"]

    cmds = read_fluent_mesh(file)

    assert cmds == tgts
    _, _ = hip_exit()

# @pytest.mark.skip(reason="SIGABRT 6, apparent hdf5 libraries version mismatch")
def test_read_cgns(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.grid.cgns')
    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read cgns %s" % 'trappedvtx.grid.cgns',
            "var"]

    cmds = read_cgns_mesh(file)

    assert cmds == tgts
    _, _ = hip_exit()

# @pytest.mark.skip(reason="SIGSEGV 11, error reading ensight mesh")
def test_read_ensight(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.case')
    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read ensight %s" % 'trappedvtx.case',
            "var"]

    cmds = read_ensight_mesh(file)

    assert cmds == tgts
    _, _ = hip_exit()

def test_read_gmsh(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.msh')

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read gmsh trappedvtx.msh",
            "var"]

    cmds = read_gmsh_mesh(file)

    assert cmds == tgts
    _, _ = hip_exit()

def test_read_centaur(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.hyb')

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "read centaur %s" % '',
            "var"]

    cmds = read_centaur_mesh(file)

#    assert cmds == tgts
    _, _ = hip_exit()

# writer commands tests
def test_write_file(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "write hdf5 new"]

    fout = datadir.join('new')
    cmds = _write_file(fout, "hdf5")

    assert cmds == tgts
    _, _ = hip_exit()

def test_write_hdf5(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "write hdf5 -7 -a new"]

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    assert cmds == tgts
    _, _ = hip_exit()

# @pytest.mark.skip('SIGSEGV 11, CGNS libray writing error,cgns not raised here')
def test_write_cgns(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "write cgns new"]

    fout = datadir.join('new')
    cmds = write_cgns(fout)

    assert cmds == tgts
    _, _ = hip_exit()

def test_write_ensight(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "write ensight -3 new"]

    fout = datadir.join('new')
    cmds = write_ensight(fout)

    assert cmds == tgts
    _, _ = hip_exit()

def test_write_fieldview(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "write fieldview new"]

    fout = datadir.join('new')
    cmds = write_fieldview(fout)

    assert cmds == tgts
    _, _ = hip_exit()

def test_write_gmsh(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "write gmsh new"]

    fout = datadir.join('new')
    cmds = write_gmsh(fout)

    assert cmds == tgts
    _, _ = hip_exit()

# @pytest.mark.skip(reason='SIGILL 4, Illegal instruction in writing avbp')
def test_write_avbp(datadir, rm_hipin):
    """functional test for meshfiles reader"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgts = ["set path %s" % os.path.dirname(os.path.abspath(file)),
            "write avbp new"]

    fout = datadir.join('new')
    cmds = write_avbp(fout)

    assert cmds == tgts
    _, _ = hip_exit()

#functional tests of operation methods
def test_adapt_with_var(datadir, rm_hipin):
    """function test for mesh adaptation using solution var"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    sol = datadir.join('trappedvtx.sol.h5')
    _ = read_hdf5_mesh(file,sol_file=sol)

    cmd = adapt_with_var('metric')

    fout = datadir.join('new')
    cmds = write_avbp(fout)

    _, _ = hip_exit()

def test_adapt_with_factor(datadir, rm_hipin):
    """test isotropic adaptation"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    sol = datadir.join('trappedvtx.sol.h5')
    _ = read_hdf5_mesh(file,sol_file=sol)

    tgt = ["mmg3d -f 1.0"]
    cmd = adapt_with_factor(1.)
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

def test_adapt_perio_with_factor(datadir, rm_hipin):
    """test isotropic adaptation with periodic mesh"""
    rm_hipin
    file = datadir.join('trappedvtx_perio.mesh.h5')
    sol = datadir.join('trappedvtx.sol.h5')
    _ = read_hdf5_mesh(file,sol_file=sol)

    tgt = ["mmg3d -f 1.0"]
    cmd = adapt_with_factor(1.)
    assert cmd == tgt

    fout = datadir.join('newperio')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

def test_set_bc(datadir, rm_hipin):
    """test on bc contents"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["set bc-text Inlet inlet"]
    cmd = set_bctext('Inlet', 'inlet')
    assert cmd == tgt

    tgt = ['set bc-type inlet n']
    cmd = set_bctype('inlet', 'n')
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

def test_set_checklevel(datadir, rm_hipin):
    """test on bc contents"""
    rm_hipin
    tgt = ["set checklevel 0"]
    cmd = set_checklevel(0)
    assert cmd == tgt

    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    tgt = ["set checklevel 1"]
    cmd = set_checklevel(1)
    assert cmd == tgt

    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    tgt = ["set checklevel 2"]
    cmd = set_checklevel(2)
    assert cmd == tgt

    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    tgt = ["set checklevel 3"]
    cmd = set_checklevel(3)
    assert cmd == tgt

    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    tgt = ["set checklevel 4"]
    cmd = set_checklevel(4)
    assert cmd == tgt

    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    tgt = ["set checklevel 5"]
    cmd = set_checklevel(5)
    assert cmd == tgt

    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    with pytest.raises(TypeError):
        assert set_checklevel(4.5)
        assert set_checklevel([3])
    with pytest.raises(ValueError):
        assert set_checklevel(6)
        assert set_checklevel(-1)

def test_interpolate(datadir, rm_hipin):
    """test on interpolation"""
    rm_hipin
    file = datadir.join('default.mesh.h5')
    sol = datadir.join('default_inst.sol.h5')
    _ = read_hdf5_mesh(file, sol_file=sol)
    _ = set_bctext('Inlet', 'inlet')
    _ = set_bctext('Outlet', 'outlet')
    _ = set_bctext('PerioLeft', 'perioleft')
    _ = set_bctext('PerioRight', 'perioright')
    _ = set_bctext('WallIn1', 'wallin1')
    _ = set_bctext('WallIn2', 'wallin2')
    _ = set_bctext('WallIn3', 'wallin3')
    _ = set_bctext('MultiperfIn', 'multiperfin')
    _ = set_bctext('WallIn4', 'wallin4')
    _ = set_bctext('InletHole', 'inlethole')
    _ = set_bctext('WallOut', 'wallout')
    _ = set_bctext('CanyonUp', 'canyonup')
    _ = set_bctext('CanyonBottom', 'canyonbottom')
    _ = set_bctext('CanyonDown', 'canyondown')
    _ = set_bctext('InletFilm', 'inletfilm')

    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["interpolate grid 1"]
    cmd = interpolate()
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

def test_transform_translate(datadir, rm_hipin):
    """test on transform contents"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["transform translate 1 0 0"]
    cmd = transform_translate(1,0,0)
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

def test_transform_scale(datadir, rm_hipin):
    """test on transform contents"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["transform scale 1 0.5 0.5"]
    cmd = transform_scale(1,0.5,0.5)
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

def test_transform_reflect(datadir, rm_hipin):
    """test on transform contents"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["transform reflect x"]
    cmd = transform_reflect('x')
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()
    
    with pytest.raises(ValueError):
        assert transform_reflect('w')

def test_transform_rotate(datadir, rm_hipin):
    """test on transform contents"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["transform rotate x 45"]
    cmd = transform_rotate('x', 45)
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    with pytest.raises(ValueError):
        assert transform_rotate('w', 45)

def test_duplicate(datadir, rm_hipin):
    """test on transform contents"""
    rm_hipin
    file = datadir.join('trappedvtx.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["copy uns 2 rotate x 40.0"]
    cmd = duplicate(2, 40.0)
    assert cmd == tgt

    tgt = ["copy uns 2 translate  0.2 0 0"]
    cmd = duplicate(2, [0.2, 0, 0], operation='translate')
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    with pytest.raises(ValueError):
        assert duplicate('w', 45.0)
        assert duplicate(2, 45)
        assert duplicate(2, 45.0, axis='w')
        assert duplicate(2, 45.0, operation='none')
        assert duplicate(2, 45.0, operation='translate')
        assert duplicate(2, [45.0, 20], operation='translate')

def test_generate(datadir, rm_hipin):
    """generation and extrusion test"""
    rm_hipin
    tgt = ["generate 0 0 1 1 6 6"]
    cmd = _generate_2d_mesh([0, 0], [1, 1], [6, 6])
    assert cmd == tgt

    tgt = ["copy 3D 0 1 6 z"]
    cmd = _extrude_2d_mesh([0, 1], 6, 'z')
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    tgt = ["generate 0 0 1 1 6 6"]
    cmd = _generate_2d_mesh([0, 0], [1, 1], [6, 6])
    assert cmd == tgt

    tgt = ["copy 3D 0 40 6 axi"]
    cmd = _extrude_2d_mesh([0, 40], 6, 'axi')
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    tgt = ["generate 0 0 1 1 6 6"]
    cmd = _generate_2d_mesh([0, 0], [1, 1], [6, 6])
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    with pytest.raises(ValueError):
        assert _generate_2d_mesh([1, 1], [0, 0], [5, 5])
        assert _extrude_2d_mesh([0, 1], 6, 'w')
        assert _extrude_2d_mesh([1, 0], 6, 'x')

def test_convert_q2t(datadir, rm_hipin):
    """conversion to tri test"""
    rm_hipin
    _ = _generate_2d_mesh([0, 0], [1, 1], [6, 6])

    tgt = ["copy q2t"]
    cmd = _convert_quad2tri()
    assert cmd == tgt

    cmd = _extrude_2d_mesh([0, 1], 6, 'x')

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    _ = _generate_2d_mesh([0, 0], [1, 1], [6, 6])

    tgt = ["copy q2t"]
    cmd = _convert_quad2tri()
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

# @pytest.mark.skip(reason="SIGSEGV 11, Segmentation fault on conversion")
def test_convert_2tets(datadir, rm_hipin):
    """conversion to tet test"""
    rm_hipin
    _ = _generate_2d_mesh([0, 0], [1, 1], [6, 6])

    cmd = _extrude_2d_mesh([0, 1], 6, 'x')

    tgt = ["copy 2tets"]
    cmd = _convert_hex2tet()
    assert cmd == tgt

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

def test_generate_mesh_2d_3d(datadir, rm_hipin):
    """full generation with conversions"""
    rm_hipin
    tgts = ["generate 0 0 1 1 6 6",
            "copy 3D 0 1 5 z"]
    cmds = generate_mesh_2d_3d((0, 0), (1, 1), (6, 6),
                               extru_axis='z', extru_range=(0, 1), extru_res=5)
#    assert tgts == cmds

    fout = datadir.join('new')
    cmds = write_hdf5(fout)

    _, _ = hip_exit()

    with pytest.raises(ValueError):
        assert generate_mesh_2d_3d((0, 0, 0), (1, 1), (6, 6),
                                   extru_axis='z', extru_range=(0, 1), extru_res=5)
        assert generate_mesh_2d_3d(0, (1, 1), (6, 6),
                                   extru_axis='z', extru_range=(0, 1), extru_res=5)
        assert generate_mesh_2d_3d((0, 0, 0), (1, 1), (6, 6),
                                   extru_axis='z', extru_range=(0, 1, 3), extru_res=5)
        assert generate_mesh_2d_3d((0, 0, 0), (1, 1), (6, 6),
                                   extru_axis='z', extru_range=0, extru_res=5)

def test_list(datadir, rm_hipin):
    """lists trivial testing"""
    rm_hipin
    file = datadir.join('new.mesh.h5')
    _ = read_hdf5_mesh(file)

    tgt = ["list surface"]
    cmd = list_surface()
    assert cmd == tgt

    tgt = ["list periodic"]
    cmd = list_periodic()
    assert cmd == tgt

    _, _ = hip_exit()
