# Copyright (C) 2022 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Tomasz Kacprzak, Silvan Fischbacher

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from trianglechain.utils_plots import (
    prepare_columns,
    setup_grouping,
    get_labels,
    get_hw_ratios,
    setup_figure,
    update_current_ranges,
    update_current_ticks,
    set_limits,
    delete_all_ticks,
    add_vline,
    get_old_lims,
    get_best_old_lims,
    find_alpha,
    get_lines_and_labels,
)
from trianglechain.params import ensure_rec
from trianglechain.make_subplots import (
    contour_cl,
    density_image,
    scatter_density,
    plot_1d,
)
from trianglechain.BaseChain import BaseChain
from tqdm.auto import tqdm, trange

from cosmic_toolbox.logger import get_logger

LOGGER = get_logger(__file__)


class TriangleChain(BaseChain):
    """
    Class to produce triangle plots of chains.
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
        tri="lower",
        plot_histograms_1D=True,
        **kwargs,
    ):
        """
        :param data: rec array
            the data that should be plotted with column data
        :param plottype: {"contour_cl", "density_image", "scatter",
            "scatter_density", "scatter_prob"}
            type of plot that should be plotted
        :param prob: None or array
            if not None, then probability attached to the samples,
            in that case samples are treated as grid not a chain
            default: None
        :param color: matplotlib color
            color of the plot, default=None (automatic)
        :param cmap: matplotlib colormap
            colormap used for this plot, default="viridis"
        :param tri: {"lower", "upper"}
            if triangle should be in the upper or lower part, default="lower"
        :param plot_histograms_1D: boolean
            if the 1D histograms should be plotted as well, default=True
        :param kwargs: additional arguments for the plotting functions, they include:
        :param cmap_vmin: fixed minimum in the colormap, default: 0
        :param cmap_vmax: fixed maximum of the colormap, default: None
        :param colorbar: if colorbar should be plotted, default: False
        :param colorbar_label: label of the colorbar, default: None
        :param colorbar_ax: position of colorbar
            default: [0.735, 0.5, 0.03, 0.25]
        :param show_values: if best-fit and uncertainty should be plotted
            default: False
        :param bestfit_method: method for the best_fit
            options: "mode", "mean", "median", "best_sample",
            default: "mode"
        :param levels_method: method to compute the uncertainty bands
            options: "hdi", "percentile", "PJ-HPD"
            default: "hdi"
        :param credible_interval: credible interval for the uncertainty
            default: 0.68
        :param lnprobs: lnprobs, only needed for best_sample and PJ-HPD
        :param scatter_vline_1D: if the scattered points should generate a
            vertical line in the 1D histograms, default: False
        :param label: label of the plot (for legend), default: None
        :param alpha1D: alpha value for the 1D plot, default: 1
        :param alpha2D: alpha value for the 2D plot, default: 1
        :param alpha_for_low_density: if to use alpha for very low density in
            density images. If True, alpha is 0 at the lowest density and
            linearly increases until the defined threshold
            default: False
        :param alpha_threshold: threshold density where alpha value should
            be 1 again
            default: 0
        :param show_legend: if legend should be shown, default: False
        """

        from copy import deepcopy

        kwargs_copy = deepcopy(self.kwargs)
        kwargs_copy.update(kwargs)

        color = self.setup_color(color)
        if (plottype == "scatter_prob") & (prob is None):
            raise ValueError("prob needs to be defined for scatter_prob")

        self.fig, self.ax = plot_triangle_marginals(
            fig=self.fig,
            size=self.size,
            func=plottype,
            cmap=cmap,
            data=data,
            prob=prob,
            tri=tri,
            color=color,
            plot_histograms_1D=plot_histograms_1D,
            **kwargs_copy,
        )
        return self.fig, self.ax


def plot_triangle_marginals(
    data,
    prob=None,
    params="all",
    params_from=None,
    names=None,
    func="contour_cl",
    tri="lower",
    single_tri=True,
    color="#0063B9",
    cmap=plt.cm.viridis,
    cmap_vmin=0,
    cmap_vmax=None,
    ranges={},
    ticks={},
    n_bins=20,
    fig=None,
    size=4,
    fill=True,
    grid=False,
    labels=None,
    plot_histograms_1D=True,
    show_values=False,
    bestfit_method="mode",
    levels_method="hdi",
    credible_interval=0.68,
    n_sigma_for_one_sided_tail=3,
    lnprobs=None,
    scatter_vline_1D=False,
    label=None,
    density_estimation_method="smoothing",
    n_ticks=3,
    tick_length=3,
    alpha1D=1,
    alpha2D=1,
    alpha_for_low_density=False,
    alpha_threshold=0,
    subplots_kwargs={},
    de_kwargs={},
    hist_kwargs={},
    line_kwargs={},
    labels_kwargs={},
    grid_kwargs={},
    scatter_kwargs={},
    grouping_kwargs={},
    axvline_kwargs={},
    add_empty_plots_like=None,
    label_fontsize=12,
    show_legend=False,
    colorbar=False,
    colorbar_label=None,
    colorbar_ax=[0.735, 0.5, 0.03, 0.25],
    normalize_prob1D=True,
    normalize_prob2D=True,
    progress_bar=True,
    **kwargs,
):
    """
    Plot a triangle plot with marginal distributions.

    :param data: rec array
        the data that should be plotted with column data
    :param prob: None or array
        probability attached to the samples, if None, then the density is estimated
        from the samples, default: None
    :param params: list of strings
        list of parameters that should be plotted, default: "all"
    :param params_from: data like array
        if params is "all", then the parameters are taken from this array
        default: None
    :param names: list
        list of names for the parameters in case data is np.ndarray, default: None
    :param func: string
        function that should be used for plotting,
        options: "contour_cl", "density_image", "scatter", "scatter_prob", "scatter_density"
        default: "contour_cl"
    :param tri: string
        if the upper or lower triangle should be plotted
        options: "upper", "lower", default: "lower"
    :param single_tri: bool
        if only one triangle should be plotted, default: True
    :param color: string
        color of the plot, default: "#0063B9"
    :param cmap: matplotlib colormap
        colormap for the density plots, default: plt.cm.viridis
    :param cmap_vmin: float
        minimum value for the colormap, default: 0
    :param cmap_vmax: float
        maximum value for the colormap, default: None
    :param ranges: dict
        dictionary with ranges for the parameters, default: {}
    :param ticks: dict
        dictionary with ticks for the parameters, default: {}
    :param n_bins: int
        number of bins for the histograms, default: 20
    :param fig: matplotlib figure
        figure that should be used for plotting, default: None
    :param size: float
        size of the plot, default: 4
    :param fill: bool
        if the contours should be filled, default: True
    :param grid: bool
        if the grid should be plotted, default: False
    :param labels: list of strings
        labels for the parameters, default: None
    :param plot_histograms_1D: bool
        if the 1D histograms should be plotted, default: True
    :param show_values: bool
        if the values should be shown in the 1D histograms, default: False
    :param bestfit_method: string
        method that should be used for the bestfit value
        options: "mode", "median", "mean", default: "mode"
    :param levels_method: string
        method that should be used for the levels
        options: "hdi", "credible_interval", default: "hdi"
    :param credible_interval: float
        credible interval for the levels, default: 0.68
    :param n_sigma_for_one_sided_tail: how many sigma should be used to decide if one
        tailed credible interval should be used
        defaults to 3
    :param lnprobs: None or array
        log probabilities attached to the samples for the level estimation,
        default: None
    :param scatter_vline_1D: bool
        if a vertical line should be plotted at the scatter points in the 1D histograms,
        default: False
    :param label: string
        label for the legend, default: None
    :param density_estimation_method: method to use for density estimation
        options: smoothing, histo, kde, gaussian_mixture, median_filter
        default: smoothing
    :param n_ticks: int
        number of ticks for the axes, default: 3
    :param tick_length: float
        length of the ticks, default: 3
    :param alpha1D: float
        alpha value for the 1D histograms, default: 1
    :param alpha2D: float
        alpha value for the 2D histograms, default: 1
    :param alpha_for_low_density: bool
        if the alpha value should be adjusted for low density regions, default: False
    :param alpha_threshold: float
        threshold for the alpha value, default: 0
    :param subplots_kwargs: dict
        keyword arguments for the subplots function, default: {}
    :param de_kwargs: dict
        keyword arguments for the density estimation, default: {}
    :param hist_kwargs: dict
        keyword arguments for the histogram, default: {}
    :param line_kwargs: dict
        keyword arguments for the lines, default: {}
    :param labels_kwargs: dict
        keyword arguments for the labels, default: {}
    :param grid_kwargs: dict
        keyword arguments for the grid, default: {}
    :param scatter_kwargs: dict
        keyword arguments for the scatter plot, default: {}
    :param grouping_kwargs: dict
        keyword arguments for the grouping, default: {}
    :param axvline_kwargs: dict
        keyword arguments for the vertical lines, default: {}
    :param add_empty_plots_like: string
        DEPRECATED, default: None
    :param label_fontsize: int
        fontsize for the labels, default: 12
    :param show_legend: bool
        if the legend should be shown, default: False
    :param colorbar: bool
        if the colorbar should be shown, default: False
    :param colorbar_label: string
        label for the colorbar, default: None
    :param colorbar_ax: list
        position of the colorbar, default: [0.735, 0.5, 0.03, 0.25]
    :param normalize_prob1D: bool
        if the 1D probability should be normalized, default: True
    :param normalize_prob2D: bool
        if the 2D probability should be normalized, default: True
    :param progress_bar: bool
        if a progress bar should be shown, default: True
    """

    ###############################
    # prepare data and setup plot #
    ###############################
    data = ensure_rec(data, names=names)
    data, columns, empty_columns = prepare_columns(
        data,
        params=params,
        params_from=params_from,
        add_empty_plots_like=add_empty_plots_like,
    )
    # needed for plotting chains with different automatic limits
    current_ranges = {}
    current_ticks = {}

    # setup everything that grouping works properly
    columns, grouping_indices = setup_grouping(columns, grouping_kwargs)
    labels = get_labels(labels, columns, grouping_indices)
    hw_ratios = get_hw_ratios(columns, grouping_kwargs)

    n_dim = len(columns)
    if single_tri:
        n_box = n_dim
    else:
        n_box = n_dim + 1

    if prob is not None:
        if np.min(prob) < 0:
            prob_offset = -np.min(prob)
        else:
            prob_offset = 0
        if normalize_prob1D:
            prob1D = (prob + prob_offset) / np.sum(prob + prob_offset)
        else:
            prob1D = None

        if normalize_prob2D:
            prob2D = (prob + prob_offset) / np.sum(prob + prob_offset)
        else:
            # for example to plot an additional parameter in parameter space
            prob_label = prob
            prob2D = None

    else:
        prob1D = None
        prob2D = None

    if tri[0] == "l":
        tri_indices = np.tril_indices(n_dim, k=-1)
    elif tri[0] == "u":
        tri_indices = np.triu_indices(n_dim, k=1)
    else:
        raise Exception("tri={} should be either lower or upper".format(tri))

    # Create figure if necessary and get axes
    fig, ax, old_tri = setup_figure(fig, n_box, hw_ratios, size, subplots_kwargs)
    if old_tri is not None and old_tri != tri:
        double_tri = True
    else:
        double_tri = False
    # get ranges for each parameter (if not specified, max/min of data is used)
    update_current_ranges(current_ranges, ranges, columns, data)

    # Bins for histograms
    hist_binedges = {
        c: np.linspace(*current_ranges[c], num=n_bins + 1) for c in columns
    }
    hist_bincenters = {
        c: (hist_binedges[c][1:] + hist_binedges[c][:-1]) / 2 for c in columns
    }

    if len(color) == len(data):
        color_hist = "k"
    else:
        color_hist = color

    def get_current_ax(ax, tri, i, j):
        if tri[0] == "u":
            if single_tri:
                axc = ax[i, j]
            else:
                axc = ax[i, j + 1]
        elif tri[0] == "l":
            if single_tri:
                axc = ax[i, j]
            else:
                axc = ax[i + 1, j]

        if i == j and not plot_histograms_1D and not scatter_vline_1D:
            # in this case axis should not be turned on in this call
            pass
        else:
            # turn on ax sinces it is used
            axc.axis("on")
        return axc

    #################
    # 1D histograms #
    #################
    if plot_histograms_1D:
        disable_progress_bar = True
        if show_values:
            LOGGER.info("Computing bestfits and levels")
            disable_progress_bar = False
        for i in trange(n_dim, disable=disable_progress_bar):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, tri, i, i)
                plot_1d(
                    axc,
                    column=columns[i],
                    param_label=labels[i],
                    data=data,
                    prob=prob1D,
                    ranges=ranges,
                    current_ranges=current_ranges,
                    hist_binedges=hist_binedges,
                    hist_bincenters=hist_bincenters,
                    density_estimation_method=density_estimation_method,
                    de_kwargs=de_kwargs,
                    show_values=show_values,
                    color_hist=color_hist,
                    empty_columns=empty_columns,
                    alpha1D=alpha1D,
                    label=label,
                    hist_kwargs=hist_kwargs,
                    fill=fill,
                    lnprobs=lnprobs,
                    levels_method=levels_method,
                    bestfit_method=bestfit_method,
                    credible_interval=credible_interval,
                    sigma_one_tail=n_sigma_for_one_sided_tail,
                    label_fontsize=label_fontsize,
                )

    if scatter_vline_1D:
        for i in range(n_dim):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, tri, i, i)
                add_vline(axc, columns[i], data, color, axvline_kwargs)

    #################
    # 2D histograms #
    #################
    for i, j in tqdm(
        zip(*tri_indices), total=len(tri_indices[0]), disable=not progress_bar
    ):
        if (columns[i] != "EMPTY") & (columns[j] != "EMPTY"):
            axc = get_current_ax(ax, tri, i, j)
            old_xlims, old_ylims = get_old_lims(axc)
            if double_tri:
                if tri == "lower":
                    other_tri = "upper"
                else:
                    other_tri = "lower"
                axc_mirror = get_current_ax(ax, other_tri, j, i)
                old_xlims_mirror, old_ylims_mirror = get_old_lims(axc_mirror)
                old_xlims, old_ylims = get_best_old_lims(
                    old_xlims, old_ylims_mirror, old_ylims, old_xlims_mirror
                )
            if (columns[i] not in data.dtype.names) | (
                columns[j] not in data.dtype.names
            ):
                pass
            elif func == "contour_cl":
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
                    alpha=min(
                        (
                            find_alpha(columns[i], empty_columns, alpha2D),
                            find_alpha(columns[j], empty_columns, alpha2D),
                        )
                    ),
                )
            elif func == "density_image":
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
                    alpha=min(
                        (
                            find_alpha(columns[i], empty_columns, alpha2D),
                            find_alpha(columns[j], empty_columns, alpha2D),
                        )
                    ),
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
            if double_tri:
                set_limits(
                    axc_mirror,
                    ranges,
                    current_ranges,
                    columns[j],
                    columns[i],
                    old_ylims,
                    old_xlims,
                )
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

    def plot_xticks(axc, i, j, length=10, direction="in"):
        if i != j:
            axc.xaxis.set_ticks_position("both")
        axc.set_xticks(get_ticks(j))
        axc.tick_params(direction=direction, length=length)

    delete_all_ticks(ax)
    update_current_ticks(current_ticks, columns, ranges, current_ranges, n_ticks)
    if tri[0] == "l" or double_tri:
        local_tri = "lower"
        for i in range(1, n_dim):  # rows
            for j in range(0, i):  # columns
                if columns[i] != "EMPTY" and columns[j] != "EMPTY":
                    axc = get_current_ax(ax, local_tri, i, j)
                    plot_yticks(axc, i, tick_length)

        for i in range(0, n_dim):  # rows
            for j in range(0, i + 1):  # columns
                if columns[i] != "EMPTY" and columns[j] != "EMPTY":
                    axc = get_current_ax(ax, local_tri, i, j)
                    plot_xticks(axc, i, j, tick_length)
    if tri[0] == "u" or double_tri:
        local_tri = "upper"
        for i in range(0, n_dim):  # rows
            for j in range(i + 1, n_dim):  # columns
                if columns[i] != "EMPTY" and columns[j] != "EMPTY":
                    axc = get_current_ax(ax, local_tri, i, j)
                    plot_yticks(axc, i, tick_length)
        for i in range(0, n_dim):  # rows
            for j in range(i, n_dim):  # columns
                if columns[i] != "EMPTY" and columns[j] != "EMPTY":
                    axc = get_current_ax(ax, local_tri, i, j)
                    plot_xticks(axc, i, j, tick_length)

    # ticklabels
    def plot_tick_labels(axc, xy, i, tri, grid_kwargs):
        ticklabels = [t for t in get_ticks(i)]
        if xy == "y":
            axc.set_yticklabels(
                ticklabels,
                rotation=0,
                fontsize=grid_kwargs["fontsize_ticklabels"],
                family=grid_kwargs["font_family"],
            )
            if tri[0] == "u":
                axc.yaxis.tick_right()
                axc.yaxis.set_ticks_position("both")
                axc.yaxis.set_label_position("right")
        elif xy == "x":
            axc.set_xticklabels(
                ticklabels,
                rotation=90,
                fontsize=grid_kwargs["fontsize_ticklabels"],
                family=grid_kwargs["font_family"],
            )
            if tri[0] == "u":
                axc.xaxis.tick_top()
                axc.xaxis.set_ticks_position("both")
                axc.xaxis.set_label_position("top")

    if tri[0] == "l" or double_tri:
        local_tri = "lower"
        # y tick labels
        for i in range(1, n_dim):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, local_tri, i, 0)
                plot_tick_labels(axc, "y", i, local_tri, grid_kwargs)
        # x tick labels
        for i in range(0, n_dim):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, local_tri, n_dim - 1, i)
                plot_tick_labels(axc, "x", i, local_tri, grid_kwargs)
    if tri[0] == "u" or double_tri:
        local_tri = "upper"
        # y tick labels
        for i in range(0, n_dim - 1):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, local_tri, i, n_dim - 1)
                plot_tick_labels(axc, "y", i, tri, grid_kwargs)
        # x tick labels
        for i in range(0, n_dim):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, local_tri, 0, i)
                plot_tick_labels(axc, "x", i, tri, grid_kwargs)

    ########
    # grid #
    ########
    if tri[0] == "l":
        for i in range(1, n_dim):
            for j in range(i):
                if columns[i] != "EMPTY" and columns[j] != "EMPTY":
                    axc = get_current_ax(ax, tri, i, j)
                    if grid:
                        axc.grid(zorder=0, linestyle="--")
                    axc.set_axisbelow(True)
    elif tri[0] == "u":
        for i in range(0, n_dim - 1):
            for j in range(i + 1, n_dim):
                if columns[i] != "EMPTY" and columns[j] != "EMPTY":
                    axc = get_current_ax(ax, tri, i, j)
                    if grid:
                        axc.grid(zorder=0, linestyle="--")
                    axc.set_axisbelow(True)

    ###########
    # legends #
    ###########
    legend_lines, legend_labels = get_lines_and_labels(ax)
    if tri[0] == "l":
        labelpad = 10
        for i in range(n_dim):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, tri, i, 0)

                axc.set_ylabel(
                    labels[i],
                    **labels_kwargs,
                    rotation=90,
                    labelpad=labelpad,
                )
                axc.yaxis.set_label_position("left")
                axc = get_current_ax(ax, tri, n_dim - 1, i)
                axc.set_xlabel(
                    labels[i], **labels_kwargs, rotation=0, labelpad=labelpad
                )
                axc.xaxis.set_label_position("bottom")
        if legend_lines and show_legend:
            # only print legend when there are labels for it
            fig.legend(
                legend_lines,
                legend_labels,
                bbox_to_anchor=(1, 1),
                bbox_transform=ax[0, n_dim - 1].transAxes,
                fontsize=label_fontsize,
            )
    elif tri[0] == "u":
        labelpad = 20
        for i in range(n_dim):
            if columns[i] != "EMPTY":
                axc = get_current_ax(ax, tri, i, n_dim - 1)
                axc.set_ylabel(
                    labels[i], **labels_kwargs, rotation=90, labelpad=labelpad
                )
                axc.yaxis.set_label_position("right")
                axc = get_current_ax(ax, tri, 0, i)
                axc.set_xlabel(
                    labels[i], **labels_kwargs, rotation=0, labelpad=labelpad
                )
                axc.xaxis.set_label_position("top")
        if legend_lines and show_legend:
            # only print legend when there are labels for it
            fig.legend(
                legend_lines,
                legend_labels,
                bbox_to_anchor=(1, 1),
                bbox_transform=ax[n_dim - 1, 0].transAxes,
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

    plt.subplots_adjust(hspace=0, wspace=0)
    fig.align_ylabels()
    fig.align_xlabels()

    for axc in ax.flatten():
        for c in axc.collections:
            if isinstance(c, mpl.collections.QuadMesh):
                # rasterize density images to avoid ugly aliasing
                # when saving as a pdf
                c.set_rasterized(True)

    return fig, ax
