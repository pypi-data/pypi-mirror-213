.. :changelog:

History
-------

0.4.1 (2023-06-09)
++++++++++++++++++

* FIX: RGB(A) colors in plt.contour

0.4.0 (2023-06-05)
++++++++++++++++++

* FEATURE: n_sigma_for_one_sided_tail free parameter to manually set the threshold when to use a 2-sided or 1-sided interval
* FIX: correct normalization when using samples with prob
* FIX: avoid upper limits with +- 0.0 and lower limits with -- 0.0

0.3.1 (2023-05-11)
++++++++++++++++++

* FIX: showing labels in most upper left corner when using only the upper triangle
* improved documentation

0.3.0 (2023-04-26)
++++++++++++++++++

* FEATURE: LineChain class to handle line chains
* FEATURE: params_from to select params from one specific input
* FEATURE: add_derived_params to add derived params to the input array
* FEATURE: new possible input type: pandas DataFrame
* FEATURE: colors are varied automatically according the matplotlib color cycle
* FEATURE: when computing bestfits and uncertainties, it automatically detects if to show bestfit +/- uncertainty or a lower/upper limit.
* FIX: ylimits in 1D plots
* FIX: tick values when choosing many ticks
* improved documentation
* dependency cleanup

0.2.1 (2023-03-20)
++++++++++++++++++

* FIX: bug in 1D histograms when using prob

0.2.0 (2023-02-09)
++++++++++++++++++

* First release on PyPI
* FEATURE: dict possible input for data
* FEATURE: argument progress_bar to disable progress_bar

0.1.2 (2023-02-02)
++++++++++++++++++

* FIX: correcting normalization of 1D posteriors (credit to Alexander Charles Tikam)

0.1.1 (2022-11-24)
++++++++++++++++++

* FIX: Bug in the number of digits

0.1.0 (2022-10-31)
++++++++++++++++++

* First release on Gitlab.
