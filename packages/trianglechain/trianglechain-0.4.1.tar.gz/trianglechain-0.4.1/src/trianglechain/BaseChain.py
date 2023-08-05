# Copyright (C) 2022 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher, Tomasz Kacprzak


from functools import partial
import matplotlib.pyplot as plt


class BaseChain:
    def __init__(self, fig=None, size=4, **kwargs):
        """
        :param fig: matplotlib figure to use
            default: None
        :param size: figures size for a new figure, for a single panel.
            All panels are square
            default: 4
        :param labels: labels for the parameters, default taken from columns
            default: None
        :param ranges: dictionary with ranges for parameters, keys correspond
            to column names
            default: {}
        :param ticks: values for axis ticks, defaults taken from range with
            equally spaced values
            default: {}
        :param n_ticks: number of ticks
            default: 3
        :param tick_length: length of the ticks
            default: 3
        :param n_bins: number of bins for 1d histograms
            default: 100
        :param fill: if to fill contours
            default: False
        :param grid: if to plot grid
            default: False
        :param add_empty_plots_like: sample with all parameters that should be
            plotted, this should be used when plotting two data sets with
            different numbers of parameters
            default: None
        :param label_fontsize: fontsize of labels in the legend and colorbar
            default: 24
        :param params: list of params that should be plotted, if all should be
            plotted use "all"
            default: "all"
        :param normalize_prob1D: if 1D probability should be normalized
            default: True
        :param normalize_prob2D: if 2D probability should be normalized
            default: True
        :param orientation: orientation for LineChain, default: "horizontal"
        :param density_estimation_method: method for density estimation with
            options:
                smoothing (default):
                    first create a histogram of samples, and then smooth it
                    with a Gaussian kernel corresponding to the variance of the
                    20% of the smallest eigenvalue of the 2D distribution
                    (smoothing scale can be adapted using the smoothing
                    parameter in the de_kwargs)
                gaussian_mixture:
                    use Gaussian mixture to fit the 2D samples
                median_filter:
                    use median filter on the 2D histogram
                kde:
                    use TreeKDE, may be slow
                hist:
                    simple 2D histogram
        :param line_space: space between lines in LineChain
        :param de_kwargs: density estimation kwargs, dictionary with keys:
            n_points:
                number of bins for 2d histograms used to create contours, etc
                default: n_bins
            levels:
                density levels for contours, the contours will enclose this
                level of probability
                default: [0.68, 0.95]
            n_levels_check:
                number of levels to check when looking for density levels
                More levels is more accurate, but slower
                default: 2000
            smoothing_parameter1D:
                smoothing scale for the 1D histograms
                default: 0.1
            smoothing_paramter2D:
                smoothing scale for the 2D histograms
                default: 0.2
        :param grid_kwargs: kwargs for the plot grid, with keys:
            fontsize_ticklabels:
                font size for tick labels, default: 14
            font_family:
                font family for tick labels, default: sans-serif
        :param hist_kwargs: kwargs for histograms, for plt.hist function
        :param labels_kwargs: kwargs for xlabels and ylabels
        :param line_kwargs: kwargs for all lines (plt.contour and plt.contourf)
        :param scatter_kwargs: kwargs for plt.scatter
        :param axvline_kwargs: kwargs for plt.axvline
        :param subplots_kwargs: kwargs for plt.subplots()
        :param grouping_kwargs: kwargs for grouping parameters in the plot with
            options:
                n_per_group: how many parameters are grouped together
                    (e.g. (3, 4, 5) for grouping the parameters accordingly)
                    default: None
                empty_ratio: fraction of a whole plot that is left empty for
                    separation
                    default: 0.2

        Basic usage:
        samples: numpy recarray containing the samples, with named columns

        tri = TriangleChain()
        tri.contour_cl(samples)  # plot contours at given confidence levels
        tri.density_image(samples)  # plot PDF density image
        tri.scatter(samples)  # simple scatter plot
        tri.scatter_prob(samples)  # scatter plot
                                   # with probability for each sample provided
        tri.scatter_density(samples) # scatter plot
                                     # color corresponds to probability
        """

        kwargs.setdefault("ticks", {})
        kwargs.setdefault("ranges", {})
        kwargs.setdefault("labels", None)
        kwargs.setdefault("n_bins", 100)
        kwargs.setdefault("de_kwargs", {})
        kwargs.setdefault("grid_kwargs", {})
        kwargs.setdefault("hist_kwargs", {})
        kwargs.setdefault("labels_kwargs", {})
        kwargs.setdefault("line_kwargs", {})
        kwargs.setdefault("axvline_kwargs", {})
        kwargs.setdefault("density_estimation_method", "smoothing")
        kwargs.setdefault("n_ticks", 3)
        kwargs.setdefault("tick_length", 3)
        kwargs.setdefault("fill", False)
        kwargs.setdefault("grid", False)
        kwargs.setdefault("scatter_kwargs", {})
        kwargs.setdefault("grouping_kwargs", {})
        kwargs.setdefault("subplots_kwargs", {})
        kwargs.setdefault("add_empty_plots_like", None)
        kwargs.setdefault("label_fontsize", 24)
        kwargs.setdefault("params", "all")
        kwargs.setdefault("line_space", 0.5)
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("normalize_prob1D", True)
        kwargs.setdefault("normalize_prob2D", True)
        kwargs.setdefault("progress_bar", True)
        kwargs["de_kwargs"].setdefault("n_points", kwargs["n_bins"])
        kwargs["de_kwargs"].setdefault("levels", [0.68, 0.95])
        kwargs["de_kwargs"].setdefault("n_levels_check", 2000)
        kwargs["de_kwargs"].setdefault("smoothing_parameter1D", 0.1)
        kwargs["de_kwargs"].setdefault("smoothing_parameter2D", 0.2)
        kwargs["de_kwargs"]["levels"].sort()
        if kwargs["fill"]:
            kwargs["line_kwargs"].setdefault("linewidths", 0.5)
        else:
            kwargs["line_kwargs"].setdefault("linewidths", 4)
        kwargs["grid_kwargs"].setdefault("fontsize_ticklabels", 14)
        kwargs["grid_kwargs"].setdefault("font_family", "sans-serif")
        kwargs["hist_kwargs"].setdefault("lw", 4)
        kwargs["labels_kwargs"].setdefault("fontsize", 24)
        kwargs["labels_kwargs"].setdefault("family", "sans-serif")
        kwargs["grouping_kwargs"].setdefault("n_per_group", None)
        kwargs["grouping_kwargs"].setdefault("empty_ratio", 0.2)

        self.fig = fig
        self.size = size
        self.kwargs = kwargs
        self.funcs = [
            "contour_cl",
            "density_image",
            "scatter",
            "scatter_prob",
            "scatter_density",
        ]
        self.colors = []

    def add_plotting_functions(self, func_add_plot):
        """
        Add plotting functions to the class.

        :param func_add_plot: function that adds a plot to the class
        """

        for fname in self.funcs:
            f = partial(func_add_plot, plottype=fname)
            doc = (
                "This function is equivalent to add_plot with \n"
                f"plottype={fname} \n" + func_add_plot.__doc__
            )
            f.__doc__ = doc
            setattr(self, fname, f)

    def setup_color(self, color):
        """
        Setup color for plotting. If color is None, find next color in cycle.

        :param color: color for plotting
        :return: color
        """

        if color is None:
            # find automatic next color
            pos_in_cycle = len(self.colors)
            colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
            self.colors.append(colors)
            return colors[pos_in_cycle % len(colors)]
        else:
            return color
