import os
from typing import Union, Iterator

import distex
import contextlib

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

from clayrs.utils.const import logger


@contextlib.contextmanager
def get_progbar(iterator, total=None) -> tqdm:
    bar_format = "{desc} {percentage:.0f}%|{bar}| {n:}/{total_fmt} [{elapsed}<{remaining}]"
    with logging_redirect_tqdm(loggers=[logger]):
        with tqdm(iterator, bar_format=bar_format, total=total) as pbar:
            yield pbar


def handle_exception(loop, context):
    # this is a simple hack to stopping asyncio from logging "task was never retrieved" exception
    # that should not happen in the first place.
    # In fact this problem happens only on specific scenarios like Pycharm interpreter, or by running
    # an asyncio snippet as script, but does not happen if the exact same script is run interactively,
    # or in IPython environment
    pass


@contextlib.contextmanager
def get_iterator_parallel(num_cpus, f_to_parallelize, *args_to_f,
                          progress_bar=False, total=None) -> Union[Iterator, tqdm]:

    num_cpus = num_cpus or os.cpu_count() or 1

    if num_cpus > 1:
        pool = distex.Pool(num_workers=num_cpus, func_pickle=distex.PickleType.cloudpickle)
        pool._loop.set_exception_handler(handle_exception)
        iterator_res = pool.map(f_to_parallelize, *args_to_f)
    else:
        pool = None
        iterator_res = map(f_to_parallelize, *args_to_f)

    try:
        if progress_bar:
            with get_progbar(iterator_res, total=total) as pbar:
                yield pbar
        else:
            yield iterator_res
    finally:
        if pool is not None:
            pool.shutdown()
