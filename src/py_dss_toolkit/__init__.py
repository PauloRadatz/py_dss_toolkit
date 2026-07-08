"""Advanced Python tools for OpenDSS built on ``py-dss-interface``.

Exports:

    __version__
        Package version string.

    CreateStudy
        Factory for snapshot and time-series power-flow studies.

    dss_tools
        Global :class:`~py_dss_toolkit.dss_tools.dss_tools.DSSTools` instance; call
        ``dss_tools.update_dss(dss)`` with a connected :class:`py_dss_interface.DSS`
        before using model, results, or views.
"""

__version__ = "0.17.0"

from .api.Creation import CreateStudy
from .dss_tools.dss_tools import dss_tools

__all__ = [
    "__version__",
    "CreateStudy",
    "dss_tools",
]
