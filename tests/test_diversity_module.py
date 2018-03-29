import os
import unittest
from pathlib import Path

from modules import DiversityModule


class test_diversity_module(unittest.TestCase):
    def test_module_tab_check(self):
        m = DiversityModule(data_workspace=str(Path(__file__).parents[1]) + os.sep + 'modules' + os.sep +
                                           'diversity_analysis')
        self.assertEqual('tab_diversity', m.get_tab_value())
