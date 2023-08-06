# -*- coding: utf-8 -*-
import optim_esm_tools as oet
import unittest
import tempfile
import matplotlib.pyplot as plt


class TestUtils(unittest.TestCase):
    def test_make_dummy_fig(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            print('created temporary directory', temp_dir)
            oet.utils.setup_plt()
            plt.scatter([1, 2], [3, 4])
            plt.legend(**oet.utils.legend_kw())
            plt.xlabel(oet.utils.string_to_mathrm('Some example x'))
            try:
                oet.utils.save_fig('bla', save_in=temp_dir)
            except RuntimeError as e:
                print(f'Most likely cause is that latex did not install, ran into {e}')

    def test_print_version(self):
        oet.utils.print_versions(['numpy', 'optim_esm_tools'])
