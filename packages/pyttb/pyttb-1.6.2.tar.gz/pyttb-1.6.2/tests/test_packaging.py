# Copyright 2022 National Technology & Engineering Solutions of Sandia,
# LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the
# U.S. Government retains certain rights in this software.

import pytest

import pyttb as ttb


def test_package_smoke():
    """A few sanity checks to make sure things don't explode"""
    assert len(ttb.__version__) > 0
    # Make sure warnings filter doesn't crash
    ttb.ignore_warnings(False)
    ttb.ignore_warnings(True)
