"""Deprecated: providence-evidence is now part of receipt-evidence.

`providence` is still the command; the code is `receipt_evidence.providence`.
This package only keeps old imports working; it will get no new features.
"""
import importlib
import sys
import warnings

__version__ = "0.2.0"

warnings.warn(
    "providence-evidence is now part of receipt-evidence; import receipt_evidence instead of providence",
    DeprecationWarning, stacklevel=2)

# Old submodule paths resolve to the new modules themselves, so
# `from providence.X import Y` and `import providence.X` keep working unchanged.
spec = sys.modules[__name__ + ".spec"] = importlib.import_module("receipt_evidence.providence.spec")
check = sys.modules[__name__ + ".check"] = importlib.import_module("receipt_evidence.providence.check")
convert = sys.modules[__name__ + ".convert"] = importlib.import_module("receipt_evidence.providence.convert")
cli = sys.modules[__name__ + ".cli"] = importlib.import_module("receipt_evidence.providence.cli")
