import sys
import pytest


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    tmpdir = request.getfixturevalue("tmpdir")
    sys.path.insert(0, str(tmpdir))
    with tmpdir.as_cwd():
        yield
