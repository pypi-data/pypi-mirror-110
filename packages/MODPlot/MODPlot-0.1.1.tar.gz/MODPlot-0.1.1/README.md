# MODPlot

[![PyPI version](https://badge.fury.io/py/MODPlot.svg)](https://pypi.org/project/MODPlot/)
[![python versions](https://img.shields.io/pypi/pyversions/MODPlot)](https://pypi.org/project/MODPlot/)

This is a standalone package version of some of the plotting functions used in the making of MOD plots. See [1908.08542](https://arxiv.org/pdf/1908.08542.pdf) for an example publication that used this style. An earlier version of this code can be found [here](https://github.com/pkomiske/MOD/blob/master/CMS2011AJets/analyzer/python/modplot.py).

## Functions

- `axes` - Makes a figure and axes in the MOD style.
- `calc_hist` - Calculates a histogram and its errors from (weighted) data.
- `style` - Gets some default style options.
- `cms_style` - Default style options for CMS data.
- `sim_style` - Default style options for SIM.
- `gen_style` - Default style options for GEN.
- `truth_style` - Default style options for truth (whatever that might be).
- `legend` - Adds a legend with the option to reorder its entries.
- `stamp` - Adds a multi-line textual "stamp" on the plot.
- `save` - Saves a plot, optionally with the MOD watermark.
- `watermark` - Adds the MOD watermark.

## Global Variables

- `PLOTS_PATH`
- `BARE_PLOTS_SUBDIR`
- `MOD_LOGO_FILEPATH`
