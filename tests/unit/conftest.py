import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """
    A single SparkSession for all unit tests.
    Local mode is fast and stable.
    """
    spark = (
        SparkSession.builder.appName("sales-metrics-unit-tests")
        .master("local[2]")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    yield spark
    spark.stop()
