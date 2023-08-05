trianglechain
=============

[![image](https://cosmo-gitlab.phys.ethz.ch/cosmo_public/trianglechain/badges/main/pipeline.svg)](https://cosmo-gitlab.phys.ethz.ch/cosmo_public/trianglechain)
[![image](http://img.shields.io/badge/arXiv-2203.09616-orange.svg?style=flat)](https://arxiv.org/abs/2203.09616)
[![image](http://img.shields.io/badge/arXiv-2207.01627-orange.svg?style=flat)](https://arxiv.org/abs/2207.01627)

Code for plotting multidimensional marginal distributions. If you use it, please cite [arXiv-2203.09616](https://arxiv.org/abs/2203.09616) and [arXiv-2207.01627](https://arxiv.org/abs/2207.01627).

[Source](https://cosmo-gitlab.phys.ethz.ch/cosmo_public/trianglechain)

[Documentation](http://cosmo-docs.phys.ethz.ch/trianglechain)


Basic Usage
-----------

To plot a standard triangle plot, you use

``` python
from trianglechain import TriangleChain
import numpy as np

# generate samples
samples = np.random.multivariate_normal(
    mean=np.zeros(3),
    cov=np.diag(np.ones(3)),
    size=(10000)
)

tri = TriangleChain()
tri.contour_cl(samples);
```
The input data can be rec arrays, numpy array, pandas dataframes or dictionaries.
For more example plots, see [demos](https://cosmo-gitlab.phys.ethz.ch/cosmo_public/trianglechain/demo)

Credits
-------

This package was created by Tomasz Kacprzak and further developed and extended by Silvan Fischbacher.
The package is maintained by Silvan Fischbacher: silvanf@phys.ethz.ch.

Contributions
-------------
Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
