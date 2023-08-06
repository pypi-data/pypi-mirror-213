"""
Processing Tools for DNPLab

Collection of processing tools for DNPLab specific to data from the Han Lab.

Thorsten Maly
Bridge12 Technologies, Inc.
"""

import numpy as _np
import dnplab as _dnp

# from .config.config import HanLab_CONFIG


def sc_integrate(data, regions):
    out = data.copy()

    out = _dnp.integrate(out, dim="f2", regions=regions)
    out = _dnp.update_axis(
        out, dim=0, new_dims="idx", start_stop=(0, len(out.values) - 1)
    )

    return out
