import os
import csv
import re
from typing import List, Dict

class DSSParser:
    """
    Parses OpenDSS scripts, expands compiled/redirected files, and flattens the script.
    Separates out simulation commands and ignores specified skipped commands.
    """
    def __init__(self, file_path: str):
        self._file_path = os.path.abspath(file_path)
        self._commands = []
        self._simulation_commands = []
        self._skipped_commands = []
        self._commented_commands = []
        self._buscoords_dict = {}
        # Hardcoded list of command verbs to skip completely
        self._skip_verbs = ["clear", "reset", "show", "plot", "visualize"]
        self._processed_files = set()
        self._current_dir = ""
        
        self.parse()

    @property
    def commands(self) -> List[str]:
        return self._commands

    @property
    def simulation_commands(self) -> List[str]:
        return self._simulation_commands

    @property
    def buscoords_dict(self) -> Dict[str, tuple]:
        return self._buscoords_dict

    @property
    def skipped_commands(self) -> List[str]:
        """Returns a list of the actual full commands that were skipped during parsing."""
        return self._skipped_commands

    @property
    def commented_commands(self) -> List[str]:
        """Returns a list of all commented commands (inline and block)."""
        return self._commented_commands

    def parse(self):
        """Starts parsing from the root file."""
        self._commands = ["clearall"]
        self._simulation_commands = []
        self._skipped_commands = []
        self._commented_commands = []
        self._buscoords_dict = {}
        self._processed_files = set()
        
        initial_dir = os.path.dirname(self._file_path)
        self._parse_file(self._file_path, initial_dir)
        
        if self._buscoords_dict:
            import tempfile
            temp_dir = tempfile.mkdtemp(prefix="pydss_")
            buscoords_path = os.path.join(temp_dir, "buscoords.csv")
            # Use forward slashes for OpenDSS path compatibility
            buscoords_path_fwd = buscoords_path.replace('\\', '/')
            buscoords_cmd = f"buscoords {buscoords_path_fwd}"
            
            with open(buscoords_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for bus, (x, y) in self._buscoords_dict.items():
                    writer.writerow([bus, x, y])
                    
            self._commands.append(buscoords_cmd)

    def get_string(self) -> str:
        """
        Returns a single string with all commands separated by newlines.
        """
        return "\n".join(self._commands)

    def _parse_file(self, file_path: str, current_dir: str):
        file_path = os.path.abspath(file_path)
        self._current_dir = current_dir
        
        if file_path in self._processed_files:
            print(f"Warning: File already processed (avoiding cycle): {file_path}")
            return
            
        self._processed_files.add(file_path)
        
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            return
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            
        # Extract and remove block comments
        block_comments = re.findall(r'(/\*.*?\*/)', text, flags=re.DOTALL)
        for bc in block_comments:
            self._commented_commands.append(bc.strip())
            
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        lines = text.splitlines()
        
        combined_lines = []
        
        for line in lines:
            # Check for inline comments
            idx_slash = line.find("//")
            idx_bang = line.find("!")
            
            if idx_slash != -1 and idx_bang != -1:
                idx = min(idx_slash, idx_bang)
            elif idx_slash != -1:
                idx = idx_slash
            elif idx_bang != -1:
                idx = idx_bang
            else:
                idx = -1
                
            if idx != -1:
                comment_text = line[idx:].strip()
                self._commented_commands.append(comment_text)
                line = line[:idx]
                
            line_strip = line.strip()
            if not line_strip:
                continue
                
            # Handle multi-line commands (~)
            if line_strip.startswith("~"):
                if combined_lines:
                    combined_lines[-1] += " " + line_strip[1:].strip()
                else:
                    combined_lines.append(line_strip[1:].strip())
            else:
                combined_lines.append(line_strip)
                
        for line in combined_lines:
            line_lower = line.lower()
            
            # buscoords
            if line_lower.startswith("buscoords"):
                self._process_buscoords(line)
                continue
                
            # compile
            if line_lower.startswith("compile"):
                self._process_compile(line)
                continue
                
            # redirect
            if line_lower.startswith("redirect"):
                self._process_redirect(line)
                continue
                
            # set datapath / data
            if line_lower.startswith("set datapath=") or line_lower.startswith("set data="):
                self._process_set_datapath(line)
                continue
                
            # skipped commands
            if any(line_lower.startswith(cmd) for cmd in self._skip_verbs):
                self._skipped_commands.append(line)
                continue
                
            # Simulation vs main commands
            if self._is_simulation_command(line_lower):
                self._simulation_commands.append(line)
            else:
                self._commands.append(line)

    def _is_simulation_command(self, line_lower: str) -> bool:
        if line_lower.startswith("solve"):
            return True
            
        if line_lower.startswith("set "):
            # We keep 'set voltagebases' in the main commands as requested
            if "voltagebases" in line_lower:
                return False
            return True
            
        return False

    def _process_buscoords(self, line: str):
        parts = line.split(maxsplit=1)
        if len(parts) > 1:
            coords_file = parts[1].strip().strip('"').strip("'").replace('\\', '/')
            full_path = os.path.abspath(os.path.join(self._current_dir, coords_file))
            
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        if len(row) == 1:
                            row = row[0].strip().replace(',', ' ').split()
                        if len(row) >= 3:
                            try:
                                bus = row[0].strip()
                                x = float(row[1].strip())
                                y = float(row[2].strip())
                                self._buscoords_dict[bus] = (x, y)
                            except ValueError:
                                continue

    def _process_compile(self, line: str):
        parts = line.split(maxsplit=1)
        if len(parts) > 1:
            referenced_path = parts[1].strip().strip('"').strip("'").replace('\\', '/')
            full_path = os.path.abspath(os.path.join(self._current_dir, referenced_path))
            
            # compile changes the directory for good in the context of the parser
            new_dir = os.path.dirname(full_path)
            self._parse_file(full_path, new_dir)
            # update current_dir to whatever directory the compile ended up in
            self._current_dir = new_dir

    def _process_redirect(self, line: str):
        parts = line.split(maxsplit=1)
        if len(parts) > 1:
            referenced_path = parts[1].strip().strip('"').strip("'").replace('\\', '/')
            full_path = os.path.abspath(os.path.join(self._current_dir, referenced_path))
            
            # redirect temporarily changes directory and then reverts back
            saved_dir = self._current_dir
            new_dir = os.path.dirname(full_path)
            self._parse_file(full_path, new_dir)
            self._current_dir = saved_dir

    def _process_set_datapath(self, line: str):
        match = re.search(r'set\s+(datapath|data)\s*=\s*(.*)', line, re.IGNORECASE)
        if match:
            path = match.group(2).strip().strip('"').strip("'").replace('\\', '/')
            full_path = os.path.abspath(os.path.join(self._current_dir, path))
            if os.path.exists(full_path):
                self._current_dir = full_path

    def save(self, output_dir: str, file_name: str):
        """
        Saves the flattened script to a new file in the specified output directory.
        Also exports the buscoords to a buscoords.csv file.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        buscoords_filename = "buscoords.csv"
        buscoords_path = os.path.join(output_dir, buscoords_filename)
        
        if self._buscoords_dict:
            with open(buscoords_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for bus, (x, y) in self._buscoords_dict.items():
                    writer.writerow([bus, x, y])
                    
        dss_path = os.path.join(output_dir, file_name)
        with open(dss_path, 'w', encoding='utf-8') as f:
            f.write("! Flattened OpenDSS script generated by py_dss_toolkit DSSParser\n")
            
            for cmd in self._commands:
                if self._buscoords_dict and cmd.lower().startswith("buscoords "):
                    f.write(f"buscoords {buscoords_filename}\n")
                else:
                    f.write(cmd + "\n")
                
            if self._simulation_commands:
                f.write("\n! --- Simulation Commands ---\n")
                for cmd in self._simulation_commands:
                    f.write(cmd + "\n")
