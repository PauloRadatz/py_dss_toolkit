=============================
py-dss-tools
=============================

**py-dss-tools** is a Python package that builds on the capabilities of the `py-dss-interface` package to provide advanced functionalities for creating Python-OpenDSS solutions more efficiently. By combining the robust connection to OpenDSS provided by `py-dss-interface` with the feature-rich tools of `py-dss-tools`, users can streamline their workflows and gain powerful new capabilities for analyzing and manipulating OpenDSS models.

For more information about `py-dss-interface`, visit its `GitHub repository <https://github.com/PauloRadatz/py_dss_interface>`_.

Key Features
============

**py-dss-tools** can be used in two main ways:

1. **Directly with the `dss_tools` Object**:
   - Import the object: ``from py_dss_tools import dss_tools``
   - Connect it to the `dss` object from `py-dss-interface`:
     ```python

        import py_dss_interface

        from py_dss_tools import dss_tools

        dss = py_dss_interface.DSS()

        dss_tools.update_dss(dss)
     ```
   - Examples are available in the folder `examples/dss_tools` or in the link `Examples of dss_tools <https://github.com/PauloRadatz/py_dss_tools/tree/master/examples/dss_tools>`_.

2. **Using the `CreateStudy` Class**:
   - Select a study type such as **static**, **temporal**, or **faultstudy**.
   - Import and create a study:
     ```python

        from py_dss_tools import CreateStudy

        study = CreateStudy.static("My Study", dss_file=dss_file)
     ```
   - Examples are available in the folder `examples/studies` or in the link `Examples of studies <https://github.com/PauloRadatz/py_dss_tools/tree/master/examples/studies>`_.

Available Features
==================

1. **Model Access and Modification**:

   - Access detailed model information through organized **pandas DataFrames**.

   - Modify models using powerful built-in functions.
   - Use via:

     - `dss_tools.model`
     - `study.model`

2. **Simulation Results**:

   - Retrieve SnapShot Power Flow results, including voltages, currents, and powers.

   - Access QSTS simulation data (e.g., energymeter and monitors).

   - Analyze FaultStudy results such as short-circuit impedances.

   - Results are tailored to the type of study created and are presented in **pandas DataFrames**.

   - Use via:

     - `dss_tools.results`
     - `study.results`

3. **Visualization**:

   - View results and circuit topology using three approaches:

     - `dss_view`: Leverages the DSSView.exe program (similar to OpenDSS).
     - `interactive_view`: Powered by Plotly for dynamic, interactive plots.
     - `static_view`: Static plots using Matplotlib.

   - Examples include:

     - Voltage profiles.
     - Time-series results.
     - Circuit topology plots.

Usage Examples
==============

Explore examples on how to use **py-dss-tools** in the following GitHub folders:

- `Examples of dss_tools <https://github.com/PauloRadatz/py_dss_tools/tree/master/examples/dss_tools>`_
- `Examples of studies <https://github.com/PauloRadatz/py_dss_tools/tree/master/examples/studies>`_

Development and Contributions
=============================

**py-dss-tools** is under continuous development. Contributions and suggestions are welcome to enhance its functionality and usability. If you have feature requests or feedback, feel free to reach out or submit issues on GitHub.

Installation
============

Install **py-dss-tools** via pip:

.. code-block:: bash

   pip install py-dss-tools

Dependencies
============

**py-dss-tools** requires **py-dss-interface**. Ensure that it is installed in your Python environment before using **py-dss-tools**.

License
=======

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
===============

Special thanks to the contributors of **py-dss-interface**, as its robust connection to OpenDSS serves as the foundation for **py-dss-tools**.

