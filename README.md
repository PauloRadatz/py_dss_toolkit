# ⚡ py-dss-toolkit: Advanced Python Tools for OpenDSS Powered by EPRI

[![PyPI Version](https://img.shields.io/pypi/v/py-dss-toolkit.svg)](https://pypi.org/project/py-dss-toolkit/)
[![License](https://img.shields.io/github/license/PauloRadatz/py_dss_toolkit)](https://github.com/PauloRadatz/py_dss_toolkit/blob/master/LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/PauloRadatz/py_dss_toolkit/python-app.yml)](https://github.com/PauloRadatz/py_dss_toolkit/actions)

**`py-dss-toolkit`** is a Python package that builds on the capabilities of the [`py-dss-interface`](https://github.com/PauloRadatz/py_dss_interface) package to provide advanced functionalities for creating Python-OpenDSS solutions more efficiently. By combining the robust connection to OpenDSS provided by `py-dss-interface` with the feature-rich tools of `py-dss-toolkit`, users can streamline their workflows and gain powerful new capabilities for analyzing and manipulating OpenDSS models, simulations, and results.

🔗 For more information about `py-dss-interface`, visit the [GitHub repository](https://github.com/PauloRadatz/py_dss_interface).

🚨 Note: This project was previously known as `py-dss-tools` and the repository was named `py_dss_tools`. It has been renamed to avoid naming conflicts on PyPI.


## 📦 Installation

You can install `py-dss-toolkit` in two ways:

### 👤 User Installation

If you simply want to use the package:

```bash
pip install py-dss-toolkit
```

### 👨‍💻 Developer Installation

If you want to contribute or explore the source code:

```bash
git clone https://github.com/PauloRadatz/py_dss_toolkit.git
cd py_dss_toolkit
pip install -e .
```

## ✨ Features

- Retrieve, analyze, and visualize OpenDSS model data using with ease.
- Flexible simulation result access via `dss_tools` or structured workflows via `CreateStudy`.
- Visualize circuit topology, voltage profiles, and time-series using DSSView, Plotly, or Matplotlib.
- Extract Simulation results directly into pandas DataFrames.
- Built on top of `py-dss-interface`.

## 🚀 What Can You Do With py-dss-toolkit?

### 🔍 1. Model Exploration and Manipulation

- Access detailed model information via organized pandas DataFrames.
- Modify models efficiently with built-in Pythonic tools.

📘 [Example Notebook](https://github.com/PauloRadatz/py_dss_toolkit/blob/master/examples/dss_tools/models.ipynb)

### 📊 2. Exploring Simulation Results Capabilities

- Retrieve SnapShot power flow results (voltages, currents, powers) via organized pandas DataFrames.
- Extract QSTS simulation data including meters and monitors.

📘 [Snapshot Results](https://github.com/PauloRadatz/py_dss_toolkit/blob/master/examples/dss_tools/snapshot_results.ipynb)
📘 [QSTS Results](https://github.com/PauloRadatz/py_dss_toolkit/blob/master/examples/dss_tools/qsts_results.ipynb)

### 📈 3. Visualize Simulation Results

`py-dss-toolkit` supports multiple methods to visualize:
- Circuit topology
- Voltage profiles
- Time-series results

All three can be visualized using:
- 🖥️ **DSSView.exe** — the native visualization tool for OpenDSS.
- 🔍 **Plotly (interactive)** — browser-based interactive plots.
- 🧾 **Matplotlib (static)** — publication-ready static charts.

📘 [Circuit Interactive View](https://github.com/PauloRadatz/py_dss_toolkit/blob/master/examples/dss_tools/circuit_interactive_view.ipynb)
📘 [Voltage Profile DSS View](https://github.com/PauloRadatz/py_dss_toolkit/blob/master/examples/dss_tools/voltage_profile_dss_view.ipynb)
📘 [Voltage Profile Interactive View](https://github.com/PauloRadatz/py_dss_toolkit/blob/master/examples/dss_tools/voltage_profile_interactive_view.ipynb)
📘 [Voltage Profile Static View](https://github.com/PauloRadatz/py_dss_tools/blob/master/examples/dss_tools/voltage_profile_static_view.ipynb)

## 🛠️ How to Use py-dss-toolkit?

### 🔧 1. Directly with the `dss_tools` Object

This approach is ideal when you want full flexibility to use `py-dss-toolkit` alongside your own custom logic or an existing `py-dss-interface` workflow. It allows you to:

- Inject the active DSS object into `py-dss-toolkit` using `update_dss()`
- Use any feature provided by `py-dss-toolkit` independently of the study type
- Combine different simulation types, preprocessing, and postprocessing in a custom flow

✅ **Pros:**
- Full control and flexibility
- Ideal for experienced users who want to mix tools freely
- Easily integrates into existing scripts

⚠️ **Cons:**
- No study-type validation (e.g., SnapShot vs QSTS restrictions)
- Higher chance of calling functions that don’t match the simulation context
- Slightly steeper learning curve for py-dss-interface beginners

```python
import py_dss_interface
from py_dss_toolkit import dss_tools

dss = py_dss_interface.DSS()
dss.text("compile path/to/model.dss")
dss_tools.update_dss(dss)

dss.text("solve")

dss_tools.interactive_view.voltage_profile()
```

### 🧪 2. Using the `CreateStudy` Class

This approach is best when you want a clear, structured workflow that restricts available features based on the type of study you are performing (e.g., SnapShot, QSTS). It abstracts the setup and ensures that only relevant tools are available, helping avoid mistakes or invalid calls.

✅ **Pros:**
- Easier for beginners to follow and use safely
- Prevents access to results or views that don’t apply to the selected study type
- Provides a cleaner, study-oriented interface

⚠️ **Cons:**
- Less flexible than using `dss_tools` directly
- You are limited to workflows supported by the framework
- More abstraction might make it harder to customize or mix multiple simulations

```python
from py_dss_toolkit import CreateStudy

study = CreateStudy.snapshot("Snapshot Study", dss_file="path/to/model.dss")
study.run()

study.interactive_view.circuit_plot()
```

## 🤝 Community and Support

Contributions and feedback are welcome! Open an issue or start a discussion on the [GitHub Issues Page](https://github.com/PauloRadatz/py_dss_tools/issues).

This project is under active development, and there are many additional features that could be included in the future. If you have ideas or specific needs, feel free to open a feature request, contribute directly, or reach out to me!

## 📚 How to Cite

If you use `py-dss-toolkit` in your academic work, please reference it as follows:

**APA Style:**

Radatz, P. (2025). *py-dss-toolkit: Advanced Python Tools for OpenDSS powered by EPRI* (Version X.X.X) [Computer software]. GitHub. https://github.com/PauloRadatz/py_dss_tools

**BibTeX Entry:**

```bibtex
@software{radatz2025pydsstools,
  author = {Paulo Radatz},
  title = {py-dss-toolkit: Advanced Python Tools for OpenDSS powered by EPRI},
  year = {2025},
  version = {X.X.X},
  url = {https://github.com/PauloRadatz/py_dss_tools}
}
```

📌 Please replace `X.X.X` with the version of the package you are using.


## 🙏 Acknowledgements
Developed and maintained by [Paulo Radatz](https://www.linkedin.com/in/pauloradatz/), with support from the global OpenDSS community.

Special thanks to the OpenDSS community and all contributors and users who have provided feedback and inspiration. The development of `py-dss-toolkit` builds on the foundation laid by [`py-dss-interface`](https://github.com/PauloRadatz/py_dss_interface).

---
