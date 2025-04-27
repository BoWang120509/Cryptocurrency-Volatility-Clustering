# Spark_Sample_Analysis.py
# ----------------------------------------------
# Purpose: Demonstrate usage of Spark RDD and DataFrame for processing
# Fulfilling the Spark RDD/DataFrame requirement of Data Processing stage
# ----------------------------------------------

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CryptoSparkAnalysis").getOrCreate()

df = spark.read.parquet("BTC-USDT.parquet")

df.printSchema()
df.createOrReplaceTempView("crypto")

query = """
SELECT year(open_time) AS year, month(open_time) AS month,
       AVG(close) AS avg_close_price,
       AVG(volume) AS avg_volume
FROM crypto
GROUP BY year, month
ORDER BY year, month
"""

monthly_summary = spark.sql(query)
monthly_summary.show(5)

# RDD MapReduce
rdd = df.select("volume").rdd.map(lambda row: row[0])
total_volume = rdd.reduce(lambda a, b: a + b)

print(f"\nTotal Trading (Map-Reduce by RDD): {total_volume}")

spark.stop()
