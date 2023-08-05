# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Silvan Fischbacher


import numpy as np
from trianglechain.bestfit import get_bestfit


def test_get_bestfit():
    np.random.seed(0)
    samples = np.random.normal(10, 1, 10000)
    lnprobs = -((samples - 10) ** 2)

    mean = get_bestfit(samples, "mean")
    median = get_bestfit(samples, "median")
    mode = get_bestfit(samples, "mode")
    best_sample = get_bestfit(samples, lnprobs, "best_sample")

    assert np.isclose(mean, 10, atol=0.1)
    assert np.isclose(median, 10, atol=0.1)
    assert np.isclose(mode, 10, atol=0.1)
    assert np.isclose(best_sample, 10, atol=0.1)
