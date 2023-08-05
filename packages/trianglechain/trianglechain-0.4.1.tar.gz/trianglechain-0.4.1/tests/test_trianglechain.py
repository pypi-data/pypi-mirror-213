# Copyright (C) 2022 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import numpy as np
import os
from trianglechain import TriangleChain


def _get_abspath(file_name):
    return os.path.join(os.path.dirname(__file__), file_name)


def get_samples(n_samples=10000, n_dims=4):
    covmat = np.random.normal(size=(n_dims, n_dims))
    covmat = np.dot(covmat.T, covmat)
    mean = np.random.uniform(size=(n_dims))
    samples = np.random.multivariate_normal(mean=mean, cov=covmat, size=(n_samples))
    from trianglechain.TriangleChain import ensure_rec

    samples = ensure_rec(samples, column_prefix="col")
    return samples


def test_basic_plot():
    samples1 = get_samples()
    samples2 = get_samples()
    tri = TriangleChain(density_estimation_method="smoothing")
    tri.contour_cl(samples1, color="r")
    tri.contour_cl(samples2, color="b")


def test_density_image():
    samples1 = get_samples()
    tri = TriangleChain(density_estimation_method="smoothing", n_bins=100)
    tri.density_image(samples1, cmap="inferno")
    tri.contour_cl(samples1, color="skyblue")


def test_scatter_density():
    samples1 = get_samples()
    tri = TriangleChain(density_estimation_method="smoothing", n_bins=100)
    tri.scatter_density(samples1, cmap="viridis")


def test_scatter_prob():
    samples = np.random.rand(1000, 5)
    prob = (10 * samples[:, 0] - 0.1) ** 3

    tri = TriangleChain(colorbar=True, colorbar_label="normalized prob")
    tri.scatter_prob(samples, prob=prob, normalize_prob2D=True, normalize_prob1D=True)

    tri = TriangleChain(colorbar=True, colorbar_label="e.g. value of 6th param")
    tri.scatter_prob(samples, prob=prob, normalize_prob2D=False, normalize_prob1D=True)

    tri = TriangleChain(colorbar=True, colorbar_label="e.g. value of 6th param")
    tri.scatter_prob(samples, prob=prob, normalize_prob2D=False, normalize_prob1D=False)


def test_scatter():
    samples = get_samples()
    tri = TriangleChain(scatter_kwargs={"s": 1}, hist_kwargs={"lw": 10})
    tri.scatter(samples, color="pink")


def test_grouping_and_double_tri():
    samples1 = get_samples(n_dims=6)
    samples2 = get_samples(n_dims=6)
    kwargs = {
        "n_ticks": 3,
        "de_kwargs": {"smoothing_parameter2D": 0.3},
        "grouping_kwargs": {"n_per_group": (4, 2), "empty_ratio": 0.2},
        "fill": True,
        "grid": True,
    }

    tri = TriangleChain(density_estimation_method="smoothing", n_bins=100, **kwargs)
    tri.contour_cl(samples1, color="r", label="sample1")
    tri.contour_cl(samples2, color="b", label="sample2", tri="upper", show_legend=True)


def test_alpha():
    samples1 = get_samples()
    samples2 = get_samples(n_dims=6)
    tri = TriangleChain(add_empty_plots_like=samples1)
    tri.contour_cl(samples1, color="r", alpha1D=0.5)
    tri.contour_cl(samples2, color="b", alpha2D=0.2)


def test_not_all_params():
    n_dims = 6
    samples1 = get_samples(n_samples=20000, n_dims=n_dims)
    samples2 = get_samples(n_samples=20000, n_dims=n_dims)
    tri = TriangleChain(params=["col0", "col2", "col5"])
    tri.contour_cl(samples1, color="r")
    tri.contour_cl(samples2, color="b")


def test_density_image_with_alpha():
    samples1 = get_samples()
    kwargs = {"alpha_for_low_density": True, "alpha_threshold": 0.1}
    tri = TriangleChain(**kwargs)
    tri.density_image(samples1, cmap="jet")
    tri.contour_cl(samples1, color="skyblue")


def test_vline():
    samples1 = get_samples()
    kwargs = {"scatter_kwargs": {"s": 500, "marker": "*", "zorder": 299}}
    tri = TriangleChain(density_estimation_method="smoothing", **kwargs)
    tri.contour_cl(samples1)
    tri.scatter(
        samples1[0],
        color="black",
        plot_histograms_1D=False,
        scatter_vline_1D=True,
    )


def test_credible_intervals():
    samples = np.load(_get_abspath("chain.npy"))
    tri = TriangleChain(params=["omega_m", "S8", "A_IA"])
    tri.contour_cl(samples, show_values=True, credible_interval=0.5)
