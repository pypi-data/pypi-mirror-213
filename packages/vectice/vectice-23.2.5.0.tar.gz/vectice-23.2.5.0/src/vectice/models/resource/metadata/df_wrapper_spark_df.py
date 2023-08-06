from __future__ import annotations

from datetime import datetime

from pyspark.sql import DataFrame as SparkDF
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, expr, lit, max, min

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
from vectice.models.resource.metadata.dataframe_config import MIN_ROWS_CAPTURE_STATS
from vectice.models.resource.metadata.df_wrapper_default import DataFrameDefaultWrapper


class SparkDFWrapper(DataFrameDefaultWrapper[SparkDF]):
    def __init__(self, dataframe: SparkDF):
        super().__init__(dataframe)
        self.spark = SparkSession.builder.getOrCreate()

    def get_size(self) -> Size:
        self.rows: int = self.dataframe.count()
        self.columns_numbers: int = len(self.dataframe.columns)

        return Size(rows=self.rows, columns=self.columns_numbers)

    def __capture_column_stats__(self, column: SparkDF, min_rows_to_compute_stats: int = MIN_ROWS_CAPTURE_STATS):
        column_type = column.dtypes[0][1]

        if column_type == "boolean":
            return (
                ColumnCategoryType.BOOLEAN,
                self.__compute_boolean_column_statistics__(column) if self.rows >= min_rows_to_compute_stats else None,
            )
        elif column_type in ["tinyint", "smallint", "int", "bigint", "float", "double", "decimal"]:
            return (
                ColumnCategoryType.NUMERICAL,
                self.__compute_numeric_column_statistics__(column) if self.rows >= min_rows_to_compute_stats else None,
            )
        elif column_type == "date" or column_type == "timestamp":
            return (
                ColumnCategoryType.DATE,
                self.__compute_date_column_statistics__(column) if self.rows >= min_rows_to_compute_stats else None,
            )
        elif column_type in ["string", "char", "varchar"]:
            return (
                ColumnCategoryType.TEXT,
                self.__compute_string_column_statistics__(column) if self.rows >= min_rows_to_compute_stats else None,
            )

        return None, None

    def __compute_boolean_column_statistics__(self, column: SparkDF):
        true_count = column.filter(column[0] == lit(True)).count()
        false_count = column.filter(column[0] == lit(False)).count()
        missing_count = column.filter(column[0].isNull()).count()

        total_count = self.dataframe.count()
        true_percentage = true_count / total_count if total_count > 0 else 0.0
        false_percentage = false_count / total_count if total_count > 0 else 0.0
        missing_percentage = missing_count / total_count if total_count > 0 else 0.0

        return BooleanStat(
            true=float(true_percentage), false=float(false_percentage), missing=float(missing_percentage)
        )

    def __compute_numeric_column_statistics__(self, column: SparkDF):
        col_name = column.columns[0]

        count = column.count()
        missing_count = column.filter(column[0].isNull()).count()
        missing_percentage = missing_count / count if count > 0 else 0.0

        statistics = column.select(col_name).summary("mean", "stddev", "min", "25%", "50%", "75%", "max")
        statistics_list = list(map(lambda row: row.asDict(), statistics.collect()))

        summary_dict = {data["summary"]: float(data[col_name]) for data in statistics_list}

        mean = summary_dict["mean"]
        std_deviation = summary_dict["stddev"]
        min_value = summary_dict["min"]
        q25 = summary_dict["25%"]
        q50 = summary_dict["50%"]
        q75 = summary_dict["75%"]
        max_value = summary_dict["max"]

        return NumericalStat(
            mean=float(mean),
            std_deviation=float(std_deviation),
            quantiles=Quantiles(
                q_min=float(min_value), q25=float(q25), q50=float(q50), q75=float(q75), q_max=float(max_value)
            ),
            missing=float(missing_percentage),
        )

    def __compute_string_column_statistics__(self, column: SparkDF):
        count = column.count()
        unique_count = column.distinct().count()

        value_counts = column.groupBy(column[0]).count().orderBy(col("count").desc()).limit(3).collect()
        most_commons = [MostCommon(str(row[0]), float(row[1] / count)) for row in value_counts]

        missing_count = column.filter(column[0].isNull()).count()
        missing_percentage = missing_count / count if count > 0 else 0.0

        return TextStat(unique=float(unique_count), missing=float(missing_percentage), most_commons=most_commons)

    def __compute_date_column_statistics__(self, column: SparkDF):
        count = column.count()
        min_date = column.select(min(column[0])).collect()[0][0].isoformat()
        max_date = column.select(max(column[0])).collect()[0][0].isoformat()

        col_name = column.columns[0]

        df = column.withColumn(col_name, column[col_name].cast("timestamp"))
        mean = datetime.isoformat(df.agg(avg(col_name).cast("timestamp").alias("avg_created_datetime")).collect()[0][0])
        df = column.withColumn(col_name, expr("UNIX_TIMESTAMP({}, 'yyyy-MM-dd')".format(col_name)))
        median = df.approxQuantile(col_name, [0.5], 0.0)[0]
        median_iso = datetime.strptime(
            self.spark.sql(f"SELECT from_unixtime({median!s}, 'yyyy-MM-dd')").collect()[0][0], "%Y-%m-%d"
        ).isoformat()

        return DateStat(
            missing=float(column.filter(column[0].isNull()).count() / count) if count > 0 else 0.0,
            minimum=str(min_date),
            mean=str(mean),
            median=str(median_iso),
            maximum=str(max_date),
        )
