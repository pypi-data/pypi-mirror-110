import unittest
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import openscienceplot_matplotlib as osp


class Test_plot(unittest.TestCase):

    def test_basic(self):

        x = np.random.random(10)
        y = np.random.random(10)

        filename = 'myfile.h5'

        if os.path.isfile(filename):
            os.remove(filename)

        with h5py.File(filename, 'w') as plot_data:

            fig, ax = plt.subplots()
            h = ax.plot(x, y)
            osp.dump(plot_data, 'mycurve', h)
            plt.close(fig)

            xy = plot_data['mycurve'][...]
            self.assertTrue(np.allclose(x, xy[:, 0]))
            self.assertTrue(np.allclose(y, xy[:, 1]))

        os.remove(filename)


class Test_errorbar(unittest.TestCase):

    def test_basic(self):

        x = np.random.random(10)
        y = np.random.random(10)
        xerr = np.random.random(10)
        yerr = np.random.random(10)

        filename = 'myfile.h5'

        if os.path.isfile(filename):
            os.remove(filename)

        with h5py.File(filename, 'w') as plot_data:

            fig, ax = plt.subplots()
            h = ax.errorbar(x, y, xerr=xerr, yerr=yerr)
            osp.dump(plot_data, 'mycurve', h)
            plt.close(fig)

            xy = plot_data['mycurve'][...]
            self.assertTrue(np.allclose(x, xy[:, 0]))
            self.assertTrue(np.allclose(y, xy[:, 1]))

        os.remove(filename)


if __name__ == '__main__':

    unittest.main()
