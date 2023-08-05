import os
import sys
import unittest

class TestImports(unittest.TestCase):

    # def setUp(self):
    #     sys.path.insert(0, '.')

    def assert_import_ok(self, str):
        try:
            exec(str)
        except:
            self.fail(str)

    def test_imports(self):
        self.assert_import_ok("import wallaroo")
        self.assert_import_ok("import wallaroo.sdk")
        self.assert_import_ok("from wallaroo.sdk import Engine")
        self.assert_import_ok("from wallaroo.sdk import Bundle")

if __name__ == '__main__':
    unittest.main()
