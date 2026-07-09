import os
import pytest
from py_dss_toolkit.utils.error_finder import ErrorFinder

@pytest.fixture
def test_files(tmp_path):
    # Valid script
    valid_file = tmp_path / "valid.dss"
    valid_file.write_text("""
    clearall
    New Circuit.Test basekv=115
    New Line.L1 phases=3 bus1=A bus2=B length=10
    """)
    
    # Script with a loading error (invalid phases)
    loading_error_file = tmp_path / "loading_error.dss"
    loading_error_file.write_text("""
    clearall
    New Circuit.Test basekv=115
    New Line.L1 phases=X bus1=A bus2=B length=10
    """)
    
    # Script with a solution error (isolated bus / disconnected load)
    # Using maxiterations=1 and a load guarantees non-convergence without crashing the DLL.
    solution_error_file = tmp_path / "solution_error.dss"
    solution_error_file.write_text("""
    clearall
    New Circuit.Test basekv=115
    New Line.L1 bus1=sourcebus bus2=A length=10
    """)
    
    return valid_file, loading_error_file, solution_error_file

def test_error_finder_valid(test_files):
    valid_file, _, _ = test_files
    finder = ErrorFinder(str(valid_file))
    
    df_load = finder.check_loading_errors()
    assert df_load.empty, "Should not find any loading errors in a valid script"
    
    df_sol = finder.check_solution_errors()
    assert df_sol.empty, "Should not find any solution errors in a valid script"

def test_error_finder_loading_error(test_files):
    _, loading_error_file, _ = test_files
    finder = ErrorFinder(str(loading_error_file))
    
    df = finder.check_loading_errors()
    assert not df.empty, "Should detect the loading error"
    
    # Verify the dataframe structure
    assert "Order" in df.columns
    assert "Command" in df.columns
    assert "Error Code" in df.columns
    assert "Description" in df.columns
    
    # Verify the error was on the bad line
    assert "phases=X" in df.iloc[0]["Command"]
    
from unittest.mock import patch, PropertyMock

def test_error_finder_solution_error(test_files):
    _, _, solution_error_file = test_files
        
    finder = ErrorFinder(str(solution_error_file))
    
    # We patch converged to False using PropertyMock to simulate a non-convergence error
    with patch('py_dss_interface.models.Solution.Solution.Solution.converged', new_callable=PropertyMock) as mock_converged:
        mock_converged.return_value = False
        # Run with solve to hit the convergence check
        df = finder.check_solution_errors(check_commands=["solve"])
        
    assert not df.empty, "Should detect the solution error"
    
    # Verify the dataframe structure
    assert "Order" in df.columns
    assert "Phase" in df.columns
    assert "Command" in df.columns
    assert "Error Code" in df.columns
    assert "Description" in df.columns
    
    assert (df["Phase"] == "Check (solve)").any(), "Should flag a check error"
