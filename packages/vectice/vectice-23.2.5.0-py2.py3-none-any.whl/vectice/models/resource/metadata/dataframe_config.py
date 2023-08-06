from typing import Union

from pandas.core.frame import DataFrame as PandasDF
from pyspark.pandas.frame import DataFrame as PysparkPandasDF
from pyspark.sql.dataframe import DataFrame as SparkDF

from vectice.models.resource.metadata.df_wrapper_resource import DataFrameWrapper

DataFramePandasType = Union[PysparkPandasDF, PandasDF]
DataFrameTypeWithoutWrapper = Union[DataFramePandasType, SparkDF]
DataFrameType = Union[DataFrameTypeWithoutWrapper, DataFrameWrapper]

MIN_ROWS_CAPTURE_STATS = 100
MAX_COLUMNS_CAPTURE_STATS = 100
