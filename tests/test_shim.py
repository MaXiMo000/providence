"""Run: python tests/test_shim.py -- the deprecated import paths still work."""
import importlib
import sys
import unittest
import warnings


class TestShim(unittest.TestCase):
    def test_old_imports_resolve_to_receipt_evidence_and_warn(self):
        sys.modules.pop("providence", None)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            import providence
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught))
        self.assertEqual(providence.__version__, "0.2.0")
        self.assertIs(importlib.import_module("providence.spec"), importlib.import_module("receipt_evidence.providence.spec"))
        self.assertIs(importlib.import_module("providence.check"), importlib.import_module("receipt_evidence.providence.check"))
        self.assertIs(importlib.import_module("providence.convert"), importlib.import_module("receipt_evidence.providence.convert"))
        self.assertIs(importlib.import_module("providence.cli"), importlib.import_module("receipt_evidence.providence.cli"))


if __name__ == "__main__":
    unittest.main()
