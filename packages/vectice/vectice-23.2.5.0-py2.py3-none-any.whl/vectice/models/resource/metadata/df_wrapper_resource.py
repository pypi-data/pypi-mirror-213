from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from vectice.models.resource.metadata.column_metadata import Column, Size

T = TypeVar("T")


class DataFrameWrapper(ABC, Generic[T]):
    """Base class for dataframe wrappers.

    Use DataFrameWrapper subclasses to assign wrap DataFrames to generate statistics  The
    Vectice library supports a handful of common cases.  Additional
    cases are generally easy to supply by deriving from this base
    class.  In particular, subclasses must override this class'
    abstact methods (`capture_columns()`, `get_size()`).
    """

    def __init__(self, dataframe: T):
        self.dataframe = dataframe

    @abstractmethod
    def capture_columns(self) -> list[Column]:
        pass

    @abstractmethod
    def get_size(self) -> Size:
        pass
