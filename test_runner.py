import os
import pathlib
import pytest

os.chdir(pathlib.Path.cwd() / 'app/tests/')

pytest.main()
