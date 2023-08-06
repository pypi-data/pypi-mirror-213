"""dbg"""

import os
from typing import Any, Callable, TypeVar

from loguru import logger
import pandas as pd

T = TypeVar("T")


def dbg(__message: str, *args: Any, **kwargs: Any) -> None:
    """dbg"""
    if os.environ.get("APP_ENV") == "development":
        logger.debug(__message, *args, **kwargs)


def print_dataframe_head(func: Callable[..., T]) -> Callable[..., T]:
    def wrapper(*args: Any, **kwargs: Any) -> T:
        result = func(*args, **kwargs)
        if os.environ.get("APP_ENV") == "development":
            if isinstance(result, pd.DataFrame):
                dbg(func.__name__)
                dbg(result.head(10))
                dbg("")
            else:
                dbg("Returned object is not a DataFrame.")
        return result

    return wrapper


def write_dataframe_to_csv(file_name: str):
    def _write_dataframe_to_csv(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            result = func(*args, **kwargs)
            if os.environ.get("SAMPLE_OUTPUT") == "True":
                if isinstance(result, pd.DataFrame):
                    directory = "sample_output"
                    os.makedirs(directory, exist_ok=True)
                    csv_filename = f"{file_name}.csv"
                    csv_path = os.path.join(directory, csv_filename)
                    result.to_csv(csv_path, index=False)
                    dbg(f"DataFrame saved to: {csv_path}")
                else:
                    dbg("Returned object is not a DataFrame.")
            return result

        return wrapper

    return _write_dataframe_to_csv
