from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Generic, TypeVar

from pandas import Series
from pyspark.sql.dataframe import DataFrame as SparkDF

from vectice.models.resource.metadata.column_metadata import Column, Size
from vectice.models.resource.metadata.dataframe_config import (
    MAX_COLUMNS_CAPTURE_STATS,
    MIN_ROWS_CAPTURE_STATS,
    DataFrameTypeWithoutWrapper,
)
from vectice.models.resource.metadata.df_wrapper_resource import DataFrameWrapper

_logger = logging.getLogger(__name__)


DT = TypeVar("DT", bound=DataFrameTypeWithoutWrapper)


class DataFrameDefaultWrapper(DataFrameWrapper[DT], Generic[DT]):
    def __init__(self, dataframe: DT):
        super().__init__(dataframe)

    @abstractmethod
    def get_size(self) -> Size:
        pass

    @abstractmethod
    def __capture_column_stats__(self, column, min_rows_to_compute_stats: int = MIN_ROWS_CAPTURE_STATS):
        pass

    def capture_columns(self) -> list[Column]:
        columns: list[Column] = []
        dtypes = self.dataframe.dtypes
        column_names_with_types = dtypes.astype(str).to_dict().items() if isinstance(dtypes, Series) else dtypes
        for idx, (name, d_type) in enumerate(column_names_with_types):
            if idx >= MAX_COLUMNS_CAPTURE_STATS:
                _logger.warning(
                    f"Statistics are only captured for the first {MAX_COLUMNS_CAPTURE_STATS} columns of your dataframe."
                )
                break
            column = self.dataframe.select(name) if isinstance(self.dataframe, SparkDF) else self.dataframe[name]
            category_type, stats = self.__capture_column_stats__(column)
            columns.append(
                Column(
                    name=name,
                    data_type=d_type if d_type != "object" else "string",
                    stats=stats,
                    category_type=category_type,
                )
            )

        return columns
