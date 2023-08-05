# Copyright (C) 2023 ETH Zurich
# Institute for Particle Physics and Astrophysics
# Author: Tomasz Kacprzak, Silvan Fischbacher

import numpy as np
import pandas as pd
from cosmic_toolbox import arraytools as at


def ensure_rec(data, names=None, column_prefix=""):
    """
    Ensure that the input data is a numpy record array (recarray).
    If the input is already a recarray, it is returned as-is.
    If it is a 2D numpy array, a pandas dataframe, or a dictionary of arrays,
    it is converted to a recarray with automatically generated field names.

    :param data: The input data to ensure is a recarray.
        If a 2D numpy array, a pandas dataframe, or a dictionary of arrays,
        it will be converted to a recarray with automatically generated field names.
    :type data: numpy.ndarray or dict or pandas.DataFrame

    :param names: A list of field names to use if the input data is a 2D numpy array.
        The length of this list should match the number of columns in the array.
        If not provided, field names will be automatically generated.
    :type names: list of str, optional

    :param column_prefix: A prefix to add to the automatically generated field names
        for the input data. This can be useful for distinguishing between multiple
        rec arrays with similar fields.
    :type column_prefix: str, optional

    :return: The input data as a recarray.
    :rtype: numpy.recarray

    Example usage:
        >>> data = np.array([[1, 2], [3, 4]])
        >>> rec = ensure_rec(data)
        >>> print(rec)
        [(1, 2) (3, 4)]

        >>> data_dict = {'a': [1, 2], 'b': [3, 4]}
        >>> rec_dict = ensure_rec(data_dict)
        >>> print(rec_dict)
        [(1, 3) (2, 4)]

        >>> data_names = np.array([[1, 2], [3, 4]])
        >>> rec_names = ensure_rec(data_names, names=['x', 'y'])
        >>> print(rec_names)
        [(1, 2) (3, 4)]

        >>> data_prefix = np.array([[1, 2], [3, 4]])
        >>> rec_prefix = ensure_rec(data_prefix, column_prefix='data_')
        >>> print(rec_prefix)
        [(1, 2) (3, 4)]

        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> rec_df = ensure_rec(df)
        >>> print(rec_df)
        [(1, 3) (2, 4)]
    """
    if isinstance(data, pd.DataFrame):
        data = data.to_records(index=False)

    if names is not None:
        assert (
            len(names) == data.shape[1]
        ), "number of names does not match the number of parameters"
        data = at.arr2rec(data, names)

    if isinstance(data, dict):
        return at.dict2rec(data)

    if data.dtype.names is not None:
        return data

    else:
        n_rows, n_cols = data.shape
        dtype = np.dtype(
            dict(
                formats=[data.dtype] * n_cols,
                names=[f"{column_prefix}{i}" for i in range(n_cols)],
            )
        )
        rec = np.empty(n_rows, dtype=dtype)
        for i in range(n_cols):
            rec[f"{column_prefix}{i}"] = data[:, i]
        return rec


def add_derived(data, new_param, derived, names=None):
    """
    Adds a new derived parameter to the input data.

    :param data: The input data to add the derived parameter to.
        If a 2D numpy array, a pandas dataframe, or a dictionary of arrays,
        it will be converted to a recarray with automatically generated field names.
    :type data: numpy.ndarray or dict or pandas.DataFrame

    :param new_param: The name of the new derived parameter to add.
    :type new_param: str

    :param derived: The derived value of the new parameter.
    :type derived: np.ndarray or list or float

    :param names: A list of field names to use if the input data is a 2D numpy array.
        The length of this list should match the number of columns in the array.
        If not provided, field names will be automatically generated.
    :type names: list of str, optional

    :return: The input data with the new derived parameter added.
    :rtype: numpy.recarray

    Example usage:

        >>> data = add_derived(data, "S8", data["sigma8"] * np.sqrt(data["omega_m"]/0.3))

    """
    # Make a rec array out of it
    data = ensure_rec(data, names=names)

    # Add new column to data
    data = at.add_cols(data, [new_param])

    # Set values of new column to the derived value
    data[new_param] = derived

    return data
