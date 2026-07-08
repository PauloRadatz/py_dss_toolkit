"""Add model test directory to path so _dss_script_runner can be imported."""

import sys
from pathlib import Path

_model_dir = Path(__file__).resolve().parent
if str(_model_dir) not in sys.path:
    sys.path.insert(0, str(_model_dir))
