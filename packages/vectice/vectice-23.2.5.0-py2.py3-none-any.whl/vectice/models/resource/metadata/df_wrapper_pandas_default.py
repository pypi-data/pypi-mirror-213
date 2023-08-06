from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

from pandas import Series, api

from vectice.models.resource.metadata.column_metadata import (
    BooleanStat,
    ColumnCategoryType,
    DateStat,
    MostCommon,
    NumericalStat,
    Quantiles,
    Size,
    TextStat,
)
from vectice.models.resource.metadata.dataframe_config import (
    MIN_ROWS_CAPTURE_STATS,
    DataFramePandasType,
)
from vectice.models.resource.metadata.df_wrapper_default import DataFrameDefaultWrapper

PT = TypeVar("PT", bound=DataFramePandasType)


class DataFrameDefaultPandasWrapper(DataFrameDefaultWrapper[PT], Generic[PT]):
    rows: int
    columns_numbers: int

    def __init__(self, dataframe: PT):
        super().__init__(dataframe)
        self.rows, self.columns_numbers = self.dataframe.shape

    @abstractmethod
    def __compute_date_column_statistics__(self, series: Series) -> DateStat:
        pass

    def get_size(self) -> Size:
        return Size(rows=int(self.rows), columns=int(self.columns_numbers))

    def is_date_series(self, column: Series) -> bool:
        if api.types.is_datetime64_any_dtype(column):
            return True

        try:
            # Temporary fixing issue -> TypeError: data type 'dbdate' not understood [EN-2534]
            if column.dtypes == "dbdate":
                return True
        except TypeError:
            pass

        return False

    def __capture_column_stats__(
        self, series: Series, min_rows_to_compute_stats: int = MIN_ROWS_CAPTURE_STATS
    ) -> tuple[ColumnCategoryType | None, TextStat | BooleanStat | NumericalStat | DateStat | None]:
        if api.types.is_bool_dtype(series):
            return (
                ColumnCategoryType.BOOLEAN,
                self.__compute_boolean_column_statistics__(series) if self.rows >= min_rows_to_compute_stats else None,
            )
        elif api.types.is_numeric_dtype(series):
            return (
                ColumnCategoryType.NUMERICAL,
                self.__compute_numeric_column_statistics__(series) if self.rows >= min_rows_to_compute_stats else None,
            )
        elif self.is_date_series(series):
            return (
                ColumnCategoryType.DATE,
                self.__compute_date_column_statistics__(series) if self.rows >= min_rows_to_compute_stats else None,
            )
        elif api.types.is_string_dtype(series) | api.types.is_categorical_dtype(series):
            return (
                ColumnCategoryType.TEXT,
                self.__compute_string_column_statistics__(series) if self.rows >= min_rows_to_compute_stats else None,
            )
        return None, None

    def __compute_boolean_column_statistics__(self, series: Series) -> BooleanStat:
        """Parse a dataframe series and return statistics about it.

        The computed statistics are:
        - The percentage of True
        - The percentage of False
        - The count missing value in %
        Parameters:
            series: The pandas series to get information from.

        Returns:
            A BooleanStat object containing the above statistics.
        """
        value_counts = series.value_counts(dropna=False)
        value_counts_percentage = value_counts / value_counts.sum()
        series_missing = series.isnull().sum()
        missing = series_missing / len(series)

        return BooleanStat(
            true=float(value_counts_percentage[True]),
            false=float(value_counts_percentage[False]),
            missing=float(missing),
        )

    def __compute_numeric_column_statistics__(self, series: Series) -> NumericalStat:
        """Parse a dataframe series and return statistics about it.

        The computed statistics are:
        - the mean
        - the standard deviation
        - the min value
        - the 25% percentiles
        - the 50% percentiles
        - the 75% percentiles
        - the max value
        - the count missing value in %
        Parameters:
            series: The pandas series to get information from.

        Returns:
            A NumericalStat object containing the above statistics.
        """
        mean = series.mean()
        std = series.std()
        min_q = series.min()
        q25 = series.quantile(0.25)
        q50 = series.quantile(0.5)
        q75 = series.quantile(0.75)
        max_q = series.max()
        missing = float(series.isnull().sum()) / float(len(series))

        return NumericalStat(
            mean=float(mean),
            std_deviation=float(std),
            quantiles=Quantiles(q_min=float(min_q), q25=float(q25), q50=float(q50), q75=float(q75), q_max=float(max_q)),
            missing=float(missing),
        )

    def __compute_string_column_statistics__(self, series: Series) -> TextStat:
        """Parse a dataframe series and return statistics about it.

        The computed statistics are:
        - the unique number of value
        - the top 3 most common values with their percentages
        - the count missing value in %
        Parameters:
            series: The pandas series to get information from.

        Returns:
            A TextStat object containing the above statistics.
        """
        missing = series.isnull().sum() / len(series)
        unique = len(series.unique())
        value_counts = series.value_counts() / series.value_counts(dropna=False).sum()

        size = 3 if unique >= 3 else unique
        value_counts_largest: Series[float] = value_counts.nlargest(size)

        return TextStat(
            unique=float(unique),
            missing=float(missing),
            most_commons=[
                MostCommon(str(i), float(value_counts_largest[i])) for i in value_counts_largest.index.values
            ],
        )
