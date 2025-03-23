import os
import pathlib

script_path = os.path.dirname(os.path.abspath(__file__))
expected_outputs = pathlib.Path(script_path).joinpath("expected_outputs")
