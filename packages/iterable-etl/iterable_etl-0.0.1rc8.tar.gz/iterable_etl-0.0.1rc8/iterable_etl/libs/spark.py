"""spark"""

from pandas import DataFrame as PandasDF
from pyspark.sql import DataFrame as SparkDF
from pyspark.sql import SparkSession


def dataframe_to_spark(df: PandasDF, spark: SparkSession) -> SparkDF:
    """
    Convert the Pandas DataFrame to a Spark DataFrame.

    from pyspark.sql import SparkSession
    spark = SparkSession.builder.getOrCreate()
    """
    spark_df = spark.createDataFrame(df)
    return spark_df


def write_to_databricks_table(spark_df: SparkDF, table_name: str) -> None:
    """
    Write the Spark DataFrame to a Databricks table.
    """
    spark_df.write.mode("overwrite").saveAsTable(table_name)
