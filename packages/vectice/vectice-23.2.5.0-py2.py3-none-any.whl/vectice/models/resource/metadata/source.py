from __future__ import annotations

import logging
from typing import Dict

from pandas.core.frame import DataFrame as PandasDF
from pyspark.pandas.frame import DataFrame as PysparkPandasDF
from pyspark.sql.dataframe import DataFrame as SparkDF

from vectice.models.resource.metadata.column_metadata import Column
from vectice.models.resource.metadata.dataframe_config import MIN_ROWS_CAPTURE_STATS, DataFrameType
from vectice.models.resource.metadata.df_wrapper_pandas import PandasDFWrapper
from vectice.models.resource.metadata.df_wrapper_pyspark_pandas import PysparkPandasDFWrapper
from vectice.models.resource.metadata.df_wrapper_resource import DataFrameWrapper
from vectice.models.resource.metadata.df_wrapper_spark_df import SparkDFWrapper

_logger = logging.getLogger(__name__)


class Source:
    def __init__(
        self,
        name: str,
        size: int | None = None,
        columns: list[Column] | None = None,
        updated_date: str | None = None,
        created_date: str | None = None,
        dataframe: DataFrameType | None = None,
    ):
        """Initialize a MetadataDB instance.

        Parameters:
            name: The name of the source.
            size: The size of the source.
            columns: The columns that compose the source.
            updated_date: The date of last update of the source.
            created_date: The date of last update of the source.
            dataframe (Optional): A dataframe allowing vectice to optionally compute more metadata about this resource such as columns stats, size, rows number and column numbers. (Support Spark, Pandas and Pandas on Spark)
        """
        self.name = name
        self.size = size
        self.columns = columns
        self.created_date = created_date
        self.updated_date = updated_date
        self._dataframe = dataframe
        self._wrapper: PandasDFWrapper | PysparkPandasDFWrapper | SparkDFWrapper | None = None

        if isinstance(self._dataframe, PandasDF):
            self._wrapper = PandasDFWrapper(self._dataframe)
        elif isinstance(self._dataframe, SparkDF):
            self._wrapper = SparkDFWrapper(self._dataframe)
        elif isinstance(self._dataframe, PysparkPandasDF):
            _logger.warning(
                "WARNING: Pandas on spark is not supported yet, pass a Pandas or a Spark DataFrame to get statistics."
            )
        elif isinstance(self._dataframe, DataFrameWrapper):
            _logger.warning(
                "WARNING: Custom wrappers are not supported yet, pass a Pandas or a Spark DataFrame to get statistics."
            )

    def asdict(self) -> dict:
        size_info: Dict[str, int | float | None] = {"rowsNumber": None, "columnsNumber": None}
        if self._wrapper is not None:
            df_info = self._wrapper.get_size()
            if df_info.rows < MIN_ROWS_CAPTURE_STATS:
                _logger.warning(
                    f"Statistics are not captured if numbers of rows are below {MIN_ROWS_CAPTURE_STATS}, to keep the data anonymous."
                )
            size_info = df_info.asdict()

        columns_list: list[Column] = self.columns if self.columns is not None else []
        columns_list = self._wrapper.capture_columns() if self._wrapper is not None else columns_list
        columns_list_dict = [col.asdict() for col in columns_list]

        return {
            **size_info,
            "size": self.size,
            "name": self.name,
            "updatedDate": self.updated_date,
            "createdDate": self.created_date,
            "columns": columns_list_dict,
        }
