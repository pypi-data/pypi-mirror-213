
import sys
import os
from pathlib import Path
import tempfile
import pytest

from partis.utils import (
  ProcessEnv,
  VirtualEnv )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_venv():

  with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir = Path(tmpdir)

    with VirtualEnv(path = tmpdir) as venv:
      assert (tmpdir / 'bin').exists()
      assert (tmpdir / 'bin' / 'python').exists()
      assert (tmpdir / 'bin' / 'python3').exists()

      with VirtualEnv(
        path = tmpdir,
        interpreter = 'python3' ) as ok:
        pass

      with pytest.raises(ValueError):
        with VirtualEnv(
          path = tmpdir / 'sub_venv',
          interpreter = venv.exec ) as bad:
          pass

    with VirtualEnv(
      path = tmpdir,
      reuse_existing = True ) as ok:
      pass



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_venv()