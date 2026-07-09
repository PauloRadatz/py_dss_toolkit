import py_dss_interface
import pandas as pd
from typing import Optional
from tqdm import tqdm
from py_dss_toolkit.utils.dss_parser import DSSParser

class ErrorFinder:
    """
    Utility to detect runtime and solution errors in OpenDSS scripts 
    using the DSSParser and a dedicated py_dss_interface.DSS engine.
    """
    def __init__(self, dss_file: str):
        self.parser = DSSParser(dss_file)
        # Create an isolated engine to avoid mutating the user's workspace
        self.dss = py_dss_interface.DSS()
        # Turn off forms to prevent pop-ups during error checking
        self.dss.dssinterface.allow_forms = 0

    def check_loading_errors(self) -> pd.DataFrame:
        """
        Executes the script sequentially and flags commands that result in a loading error.
        Returns a DataFrame with 'Order', 'Command', 'Error Code', and 'Description'.
        """
        self.dss.text("clear")
        errors = []
        error_order = 1
        
        for cmd in tqdm(self.parser.commands, desc="Checking loading errors"):
            cmd_ascii = cmd.encode("ascii", errors="ignore").decode()
            self.dss.text(cmd_ascii)
            
            err_code = self.dss.errorinterface.error_code
            if err_code != 0:
                errors.append({
                    "Order": error_order,
                    "Command": cmd_ascii,
                    "Error Code": err_code,
                    "Description": self.dss.errorinterface.error_desc
                })
                error_order += 1
                
        return pd.DataFrame(errors)

    def check_solution_errors(self, simulation_commands: Optional[list] = None, check_commands: Optional[list] = None) -> pd.DataFrame:
        """
        Executes the script sequentially. After the circuit element is instantiated, 
        injects simulation commands. Then, after every subsequent command, it runs 
        the check_commands (like 'solve' or '_SolveDirect') to detect errors.
        
        Args:
            simulation_commands: Commands to run exactly once after the circuit is created.
                                 Defaults to ["set controlmode=static", "set mode=snapshot"].
            check_commands: Commands to run after EVERY component addition to check for errors.
                            Defaults to ["_SolveDirect"].
        """
        if simulation_commands is None:
            simulation_commands = ["set controlmode=static", "set mode=snapshot"]
        if check_commands is None:
            check_commands = ["_SolveDirect"]
            
        self.dss.text("clear")
        errors = []
        error_order = 1
        sim_commands_injected = False
        
        for cmd in tqdm(self.parser.commands, desc="Checking solution errors"):
            cmd_ascii = cmd.encode("ascii", errors="ignore").decode()
            self.dss.text(cmd_ascii)
            
            err_code = self.dss.errorinterface.error_code
            if err_code != 0:
                errors.append({
                    "Order": error_order,
                    "Phase": "Loading",
                    "Command": cmd_ascii,
                    "Error Code": err_code,
                    "Description": self.dss.errorinterface.error_desc
                })
                error_order += 1
                
            # Inject simulation commands right after the circuit is created
            if not sim_commands_injected and self.dss.circuit.name != "":
                for sim_cmd in simulation_commands:
                    sim_cmd_ascii = sim_cmd.encode("ascii", errors="ignore").decode()
                    self.dss.text(sim_cmd_ascii)
                sim_commands_injected = True
                
            # If circuit exists, run the stress test commands (solve, _SolveDirect, etc.)
            if sim_commands_injected:
                for check_cmd in check_commands:
                    self.dss.text(check_cmd)
                    
                    if check_cmd.lower() == "solve" and not self.dss.solution.converged:
                        errors.append({
                            "Order": error_order,
                            "Phase": f"Check ({check_cmd})",
                            "Command": cmd_ascii,
                            "Error Code": -1, # Custom code for non-convergence
                            "Description": "Did not converge after solve."
                        })
                        error_order += 1
                    else:
                        check_err_code = self.dss.errorinterface.error_code
                        check_err_desc = self.dss.errorinterface.error_desc
                        
                        # Some commands like _SolveDirect might cause a DLL exception but return error_code 0
                        # They will, however, populate error_desc. We clear error_desc if it succeeds.
                        if check_err_code != 0 or check_err_desc.strip() != "":
                             errors.append({
                                "Order": error_order,
                                "Phase": f"Check ({check_cmd})",
                                "Command": cmd_ascii,
                                "Error Code": check_err_code,
                                "Description": check_err_desc
                            })
                             error_order += 1
                             
        return pd.DataFrame(errors)
