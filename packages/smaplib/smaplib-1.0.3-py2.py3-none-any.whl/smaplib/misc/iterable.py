from __future__ import annotations

import itertools as it
from collections.abc import Iterable
from typing import Any
from typing import Tuple

import pandas as pd


def chunks(iterable: Iterable, batch_size: int) -> Iterable:
    """
    Divide an iterable into chunks of a specified size.

    Args:
        iterable (iterable): The iterable to divide into chunks.
        batch_size (int): The size of each chunk.

    Yields:
        tuple: The next chunk of the iterable as a tuple.

    """
    ite = iter(iterable)
    chunk = tuple(it.islice(ite, batch_size))

    while chunk:
        yield chunk
        chunk = tuple(it.islice(ite, batch_size))


def iterate_dataframe(df: pd.DataFrame, return_index: bool) -> Iterable:
    """
    Iterate over a dataframe.
    """
    for row in df.itertuples(index=return_index):
        yield row._asdict()


def chunks_dataframe(df: pd.DataFrame, batch_size: int, return_index: bool) -> Iterable:
    """
    Divide a dataframe into chunks of a specified size.
    """
    for chunk in chunks(iterate_dataframe(df, return_index), batch_size):
        yield chunk
