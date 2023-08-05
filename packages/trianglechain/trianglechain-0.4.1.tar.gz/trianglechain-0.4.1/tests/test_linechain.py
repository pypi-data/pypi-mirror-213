# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher

import numpy as np
from trianglechain import LineChain


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
    tri = LineChain()
    tri.contour_cl(samples1, color="r")
    tri.contour_cl(samples2, color="b")
