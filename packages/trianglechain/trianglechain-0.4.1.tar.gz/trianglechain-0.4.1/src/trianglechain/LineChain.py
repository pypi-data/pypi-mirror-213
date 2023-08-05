# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher, Tomasz Kacprzak

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from trianglechain.utils_plots import (
    prepare_columns,
    update_current_ranges,
    set_limits,
    get_old_lims,
    update_current_ticks,
    delete_all_ticks,
    get_lines_and_labels,
    get_labels,
)
from trianglechain.params import ensure_rec
from trianglechain.make_subplots import (
    contour_cl,
    density_image,
    scatter_density,
)
from trianglechain.BaseChain import BaseChain


class LineChain(BaseChain):
    """
    Class to produce line plots of chains
    """

    def __init__(self, fig=None, size=4, **kwargs):
        super().__init__(fig=fig, size=size, **kwargs)

        self.add_plotting_functions(self.add_plot)

    def add_plot(
        self,
        data,
        plottype,
        prob=None,
        color=None,
        cmap=plt.cm.viridis,
        **kwargs,
    ):
        """
        Add a plot to the figure.
        """

        from copy import deepcopy

        kwargs_copy = deepcopy(self.kwargs)
        kwargs_copy.update(kwargs)

        if (plottype == "scatter_prob") & (prob is None):
            raise ValueError("prob needs to be defined for scatter_prob")

        color = self.setup_color(color)
        self.fig = plot_line_marginals(
            fig=self.fig,
            size=self.size,
            func=plottype,
            cmap=cmap,
            data=data,
            prob=prob,
            color=color,
            **kwargs_copy,
        )

        return self.fig


def get_param_pairs(n_output):
    """
    Get all pairs of parameters.

    :param n_output: number of parameters
    """

    pairs = []
    for i in range(n_output):
        for j in range(i + 1, n_output):
            pairs += [[i, j]]
    return pairs


def plot_line_marginals(
    data,
    prob=None,
    params="all",
    params_from=None,
    names=None,
    func="contour_cl",
    orientation="horizontal",
    color="#0063B9",
    cmap=plt.cm.viridis,
    cmap_vmin=0,
    cmap_vmax=None,
    colorbar=False,
    colorbar_label=None,
    colorbar_ax=[0.735, 0.5, 0.03, 0.25],
    ranges={},
    ticks={},
    n_ticks=3,
    tick_length=3,
    n_bins=20,
    fig=None,
    size=4,
    fill=True,
    grid=False,
    labels=None,
    label=None,
    label_fontsize=12,
    show_legend=False,
    line_space=0.5,
    density_estimation_method="smoothing",
    alpha=1,
    alpha_for_low_density=False,
    alpha_threshold=0,
    subplots_kwargs={},
    de_kwargs={},
    labels_kwargs={},
    grid_kwargs={},
    line_kwargs={},
    scatter_kwargs={},
    normalize_prob2D=True,
    **kwargs,
):
    """
    Plot line plots of chains.

    :param data: rec array, array, dict or pd dataframe
        data to plot
    :param prob: probability for each sample
    :param params: parameters to plot, default: "all"
    :param params_from: chain to get parameters from, default: None
    :param names: names of parameters (when data is np array), default: None
    :param func: function to use for plotting
        options: contour_cl, density_image, scatter_density, scatter_prob, scatter
        default: contour_cl
    :param orientation: orientation of the plots,
        options: horizontal, vertical
        default: horizontal
    :param color: color of the plot, default: "#0063B9"
    :param cmap: colormap for 2D plots, default: plt.cm.viridis
    :param cmap_vmin: minimum value for colormap, default: 0
    :param cmap_vmax: maximum value for colormap, default: None
    :param colorbar: show colorbar, default: False
    :param colorbar_label: label for colorbar, default: None
    :param colorbar_ax: position of colorbar, default: [0.735, 0.5, 0.03, 0.25]
    :param ranges: dictionary with ranges for each parameter, default: {}
    :param ticks: dictionary with ticks for each parameter, default: {}
    :param n_ticks: number of ticks for each parameter, default: 3
    :param tick_length: length of ticks, default: 3
    :param n_bins: number of bins for histograms, default: 20
    :param fig: figure to plot on, default: None
    :param size: size of the figure, default: 4
    :param fill: fill the area of the contours, default: True
    :param grid: show grid, default: False
    :param labels: labels for each parameter, default: None
        if None, labels are taken from the parameter names
    :param label: label for the plot, default: None
    :param label_fontsize: fontsize of the label, default: 12
    :param show_legend: show legend, default: False
    :param line_space: space between plots, default: 0.5
    :param density_estimation_method: method to use for density estimation
        options: smoothing, histo, kde, gaussian_mixture, median_filter
        default: smoothing
    :param alpha: alpha value for the plot, default: 1
    :param alpha_for_low_density: use alpha for low density regions, default: False
    :param alpha_threshold: threshold for alpha, default: 0
    :param subplots_kwargs: kwargs for plt.subplots, default: {}
    :param de_kwargs: kwargs for density estimation, default: {}
    :param labels_kwargs: kwargs for labels, default: {}
    :param grid_kwargs: kwargs for grid, default: {}
    :param line_kwargs: kwargs for line plots, default: {}
    :param scatter_kwargs: kwargs for scatter plots, default: {}
    :param normalize_prob2D: normalize probability for 2D plots, default: True
    :param kwargs: additional kwargs for the plot function
    :return: fig, axes
    """
    ###############################
    # prepare data and setup plot #
    ###############################
    data = ensure_rec(data, names=names)
    data, columns, _ = prepare_columns(
        data,
        params=params,
        params_from=params_from,
    )
    # needed for plotting chains with different automatic limits
    current_ranges = {}
    current_ticks = {}

    labels = get_labels(labels, columns)
    n_dim = len(columns)

    if prob is not None:
        if np.min(prob) < 0:
            prob_offset = -np.min(prob)
        else:
            prob_offset = 0
        if normalize_prob2D:
            prob2D = (prob + prob_offset) / np.sum(prob + prob_offset)
        else:
            # for example to plot an additional parameter in parameter space
            prob_label = prob
            prob2D = None

    if orientation[0] == "h":
        n_rows = 1
        n_cols = (n_dim**2 - n_dim) // 2
    elif orientation[0] == "v":
        n_cols = 1
        n_rows = (n_dim**2 - n_dim) // 2

    # Create figure if necessary and get axes
    if fig is None:
        fig, _ = plt.subplots(
            nrows=n_rows,
            ncols=n_cols,
            figsize=(n_cols * size, n_rows * size * 0.7),
            **subplots_kwargs,
        )
        if orientation[0] == "h":
            fig.subplots_adjust(wspace=line_space)
        else:
            fig.subplots_adjust(hspace=line_space)
        ax = np.array(fig.get_axes()).ravel().reshape(n_rows, n_cols)
    else:
        ax = np.array(fig.get_axes()).ravel().reshape(n_rows, n_cols)

    # get ranges for each parameter (if not specified, max/min of data is used)
    update_current_ranges(current_ranges, ranges, columns, data)

    def get_current_ax(ax, i):
        if orientation[0] == "h":
            axc = ax[0, i]
        elif orientation[0] == "v":
            axc = ax[i, 0]
        return axc

    #################
    # 2D histograms #
    #################
    pairs = get_param_pairs(n_dim)
    for k, (i, j) in enumerate(pairs):
        axc = get_current_ax(ax, k)
        old_xlims, old_ylims = get_old_lims(axc)
        if func == "contour_cl":
            contour_cl(
                axc,
                data=data,
                ranges=current_ranges,
                columns=columns,
                i=i,
                j=j,
                fill=fill,
                color=color,
                de_kwargs=de_kwargs,
                line_kwargs=line_kwargs,
                prob=prob,
                density_estimation_method=density_estimation_method,
                label=label,
                alpha=alpha,
            )

        if func == "density_image":
            density_image(
                axc,
                data=data,
                ranges=current_ranges,
                columns=columns,
                i=i,
                j=j,
                cmap=cmap,
                de_kwargs=de_kwargs,
                vmin=cmap_vmin,
                vmax=cmap_vmax,
                prob=prob,
                density_estimation_method=density_estimation_method,
                label=label,
                alpha_for_low_density=alpha_for_low_density,
                alpha_threshold=alpha_threshold,
            )

        elif func == "scatter":
            axc.scatter(
                data[columns[j]],
                data[columns[i]],
                c=color,
                label=label,
                alpha=alpha,
                **scatter_kwargs,
            )

        elif func == "scatter_prob":
            if normalize_prob2D:
                _prob = prob2D
            else:
                _prob = prob_label
            sorting = np.argsort(_prob)
            axc.scatter(
                data[columns[j]][sorting],
                data[columns[i]][sorting],
                c=_prob[sorting],
                label=label,
                cmap=cmap,
                **scatter_kwargs,
            )

        elif func == "scatter_density":
            scatter_density(
                axc,
                points1=data[columns[j]],
                points2=data[columns[i]],
                n_bins=n_bins,
                lim1=current_ranges[columns[j]],
                lim2=current_ranges[columns[i]],
                norm_cols=False,
                n_points_scatter=-1,
                cmap=cmap,
                label=label,
            )
        set_limits(
            axc,
            ranges,
            current_ranges,
            columns[i],
            columns[j],
            old_xlims,
            old_ylims,
        )
    # grid
    for axc in ax.flatten():
        axc.grid(grid)

    #########
    # ticks #
    #########

    def get_ticks(i):
        try:
            return ticks[columns[i]]
        except Exception:
            return current_ticks[columns[i]]

    def plot_yticks(axc, i, length=10, direction="in"):
        axc.yaxis.set_ticks_position("both")
        axc.set_yticks(get_ticks(i))
        axc.tick_params(direction=direction, length=length)

    def plot_xticks(axc, i, length=10, direction="in"):
        axc.xaxis.set_ticks_position("both")
        axc.set_xticks(get_ticks(j))
        axc.tick_params(direction=direction, length=length)

    delete_all_ticks(ax)
    update_current_ticks(current_ticks, columns, ranges, current_ranges, n_ticks)

    for k, (i, j) in enumerate(pairs):
        axc = get_current_ax(ax, k)
        plot_xticks(axc, j, tick_length)
        plot_yticks(axc, i, tick_length)

    def plot_tick_labels(axc, xy, i, grid_kwargs):
        ticklabels = [t for t in get_ticks(i)]
        if xy == "y":
            axc.set_yticklabels(
                ticklabels,
                rotation=0,
                fontsize=grid_kwargs["fontsize_ticklabels"],
                family=grid_kwargs["font_family"],
            )
        elif xy == "x":
            axc.set_xticklabels(
                ticklabels,
                rotation=90,
                fontsize=grid_kwargs["fontsize_ticklabels"],
                family=grid_kwargs["font_family"],
            )

    for k, (i, j) in enumerate(pairs):
        axc = get_current_ax(ax, k)
        plot_tick_labels(axc, "x", j, grid_kwargs)
        plot_tick_labels(axc, "y", i, grid_kwargs)

    # legends
    legend_lines, legend_labels = get_lines_and_labels(ax)
    for k, (i, j) in enumerate(pairs):
        labelpad = 10
        axc = get_current_ax(ax, k)
        axc.set_ylabel(
            labels[i],
            **labels_kwargs,
            rotation=90,
            labelpad=labelpad,
        )
        axc.yaxis.set_label_position("left")
        axc.set_xlabel(labels[j], **labels_kwargs, rotation=0, labelpad=labelpad)
        axc.xaxis.set_label_position("bottom")
        if legend_lines and show_legend:
            # only print legend when there are labels for it
            fig.legend(
                legend_lines,
                legend_labels,
                bbox_to_anchor=(1, 1),
                bbox_transform=ax[0, -1].transAxes,
                fontsize=label_fontsize,
            )

    if colorbar:
        try:
            cmap_vmin = min(prob_label)
            cmap_vmax = max(prob_label)
        except Exception:
            pass
        norm = mpl.colors.Normalize(vmin=cmap_vmin, vmax=cmap_vmax)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        # sm.set_array([])
        # ticks = np.linspace(amin, amax, 3)
        cbar = fig.colorbar(sm, cax=fig.add_axes(colorbar_ax))
        cbar.ax.tick_params(labelsize=grid_kwargs["fontsize_ticklabels"])
        cbar.set_label(colorbar_label, fontsize=label_fontsize)

    for axc in ax.flatten():
        for c in axc.collections:
            if isinstance(c, mpl.collections.QuadMesh):
                # rasterize density images to avoid ugly aliasing
                # when saving as a pdf
                c.set_rasterized(True)
    return fig
