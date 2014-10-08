"""Check the syntax in example files is valid"""

import unittest
from unittest import TestCase
import tempfile
import os
import sys


class TestExamples(TestCase):
    def setUp(self):
        # Run in a tempdir, in case the examples dump any output
        self.orig_dir = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

        repo_topdir = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__)))
        self.examples_dir = os.path.join(repo_topdir, 'examples')
        sys.path.insert(0, self.examples_dir)

    def tearDown(self):
        os.chdir(self.orig_dir)
        sys.path.pop(0)

    def test_basic_usage(self):
        import basic_usage

    def test_new_voevent(self):
        import author_new_voevent





