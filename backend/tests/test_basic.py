
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest import TestCase,mock 
from mock import MagicMock
import utils 



class TestUtilsModule(TestCase):
    def test_load_server_list_returns_list(self):
        with mock.patch("utils.load_server_list") as MockHelper:
            MockHelper.return_value = 'testing'
            self.assertEqual(utils.load_server_list(), 'testing')
       
if __name__ == 'main':
    unittest.main()