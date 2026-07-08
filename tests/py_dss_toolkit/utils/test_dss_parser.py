import os
import pytest
from py_dss_toolkit.utils.dss_parser import DSSParser

@pytest.fixture
def temp_dss_files(tmp_path):
    # Create main.dss
    main_file = tmp_path / "main.dss"
    main_content = """
    clear
    ! this is a comment
    New Circuit.Test
    ~ basekv=115 pu=1.0001
    
    // another comment
    /* block 
       comment */
    
    set voltagebases=[115, 12.47]
    calcvoltagebases
    
    compile "subfolder/lines.dss"
    
    solve
    show voltages
    """
    main_file.write_text(main_content)
    
    # Create subfolder/lines.dss
    subfolder = tmp_path / "subfolder"
    subfolder.mkdir()
    lines_file = subfolder / "lines.dss"
    lines_content = """
    New Line.L1 phases=3 bus1=A bus2=B length=10
    
    redirect "loads.dss"
    
    buscoords "coords.csv"
    """
    lines_file.write_text(lines_content)
    
    # Create subfolder/loads.dss
    loads_file = subfolder / "loads.dss"
    loads_content = """
    New Load.Load1 phases=3 bus1=B kW=100 kvar=50
    """
    loads_file.write_text(loads_content)
    
    # Create subfolder/coords.csv
    coords_file = subfolder / "coords.csv"
    coords_content = """
    A, 1.0, 2.0
    B, 3.0, 4.0
    """
    coords_file.write_text(coords_content)
    
    return main_file, tmp_path

def test_dss_parser_parsing(temp_dss_files):
    main_file, tmp_path = temp_dss_files
    
    parser = DSSParser(str(main_file))
    
    # Check skipped commands
    assert "clear" not in parser.commands
    assert "show voltages" not in parser.commands
    assert "clear" in parser.skipped_commands
    assert "show voltages" in parser.skipped_commands
    
    # Check commented commands
    assert "! this is a comment" in parser.commented_commands
    assert "// another comment" in parser.commented_commands
    assert "/* block \n       comment */" in parser.commented_commands
    
    # Check simulation commands
    assert "solve" in parser.simulation_commands
    
    # Check main commands
    assert "clearall" in parser.commands
    assert "calcvoltagebases" in parser.commands
    assert "New Circuit.Test basekv=115 pu=1.0001" in parser.commands
    assert "set voltagebases=[115, 12.47]" in parser.commands
    assert "New Line.L1 phases=3 bus1=A bus2=B length=10" in parser.commands
    assert "New Load.Load1 phases=3 bus1=B kW=100 kvar=50" in parser.commands
    
    # Check buscoords
    assert parser.buscoords_dict == {"A": (1.0, 2.0), "B": (3.0, 4.0)}
    
    # Check string generation
    full_str = parser.get_string()
    assert "clearall" in full_str
    assert "buscoords" in full_str
    assert "calcvoltagebases" in full_str
    assert "solve" not in full_str  # only commands, not simulation_commands
    
def test_dss_parser_save(temp_dss_files):
    main_file, tmp_path = temp_dss_files
    
    parser = DSSParser(str(main_file))
    
    out_dir = tmp_path / "output"
    parser.save(str(out_dir), "flattened.dss")
    
    # Verify files are saved
    assert (out_dir / "flattened.dss").exists()
    assert (out_dir / "buscoords.csv").exists()
    
    # Read saved dss file and verify contents
    saved_text = (out_dir / "flattened.dss").read_text()
    
    assert "clearall" in saved_text
    assert "New Circuit.Test basekv=115 pu=1.0001" in saved_text
    assert "New Line.L1 phases=3 bus1=A bus2=B length=10" in saved_text
    assert "buscoords buscoords.csv" in saved_text
    assert "solve" in saved_text
    assert "calcvoltagebases" in saved_text
