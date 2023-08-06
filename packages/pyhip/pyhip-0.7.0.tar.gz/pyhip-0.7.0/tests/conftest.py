import os

from distutils import dir_util

import pytest

@pytest.fixture(scope='module')
def datadir(tmpdir_factory, request):
    '''
    Fixture responsible for searching a folder with the same name as test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    file_path = request.module.__file__
    test_dir, _ = os.path.splitext(file_path)
    dir_name = os.path.basename(test_dir)

    datadir_ = tmpdir_factory.mktemp(dir_name)
    dir_util.copy_tree(test_dir, str(datadir_))

    return datadir_

@pytest.fixture(scope='module')
def rm_hipin():
    '''
    Fixture responsible for searching a folder with the same name as test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    file = os.path.abspath("%d_hip.in" % os.getpid())
    if os.path.isfile(file):
        os.remove(file)
