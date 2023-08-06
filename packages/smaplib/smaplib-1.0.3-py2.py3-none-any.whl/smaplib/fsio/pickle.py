from __future__ import annotations

import os as os
import pickle as pk

import numpy as np


def save_to_pickle(file_path, data):
    """Saves a Python object to a pickle file at the specified file path.

    Args:
        file_path (str): The file path where the pickle file should be saved.
        data (any): The Python object to be saved.

    Returns:
        str: The file path of the saved pickle file.
    """
    with open(file_path, "wb") as fp:
        pk.dump(data, fp, protocol=pk.HIGHEST_PROTOCOL)
    return file_path


def load_from_pickle(file_path):
    """Loads a Python object from a pickle file at the specified file path.

    Args:
        file_path (str): The file path of the pickle file to be loaded.

    Returns:
        any: The Python object loaded from the pickle file.
    """
    with open(file_path, "rb") as fp:
        data = pk.load(fp)
    return data
