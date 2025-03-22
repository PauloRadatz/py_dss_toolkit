import os
import py_dss_tools

dss_file = r"C:\Users\paulo\OneDrive\Desktop\123Bus\IEEE123Master.dss"

st = py_dss_tools.CreateStudy.snapshot("Test 1", dss_file)

st.dss.text("New EnergyMeter.Feeder Line.L115 1")
st.dss.text("solve")

print(os.path.dirname(os.path.abspath(__file__)))

st.view.voltage_profile()
