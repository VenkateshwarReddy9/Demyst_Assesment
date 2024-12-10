import hashlib
import csv
import os
from pyspark.sql import SparkSession 
from pyspark.sql.functions import sha2, concat_ws, lit  

# Function to determine file size in GB
def get_file_size(file_path):
    return os.path.getsize(file_path) / (1024 ** 3)

# Anonymization function for local processing
def anonymize(value, salt="random_salt"):
    return hashlib.sha256(f"{value}{salt}".encode("utf-8")).hexdigest()

# Local processing: anonymize CSV with chunking
def anonymize_csv_locally(input_file, output_file, chunk_size=100_000):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()

        buffer = []
        for row in reader:
            row["first_name"] = anonymize(row["first_name"])
            row["last_name"] = anonymize(row["last_name"])
            row["address"] = anonymize(row["address"])
            buffer.append(row)

            if len(buffer) >= chunk_size:
                writer.writerows(buffer)
                buffer.clear()

        if buffer:
            writer.writerows(buffer)
    print(f"Data anonymization completed (locally): {output_file}")

# Spark-based distributed processing
def anonymize_csv_with_spark(input_file, output_file, salt="random_salt"):
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("CSV Anonymization") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()

    # Load the CSV into a Spark DataFrame
    df = spark.read.csv(input_file, header=True, inferSchema=True)

    # Anonymize columns with hashing and salting
    anonymized_df = df.withColumn("first_name", sha2(concat_ws("", "first_name", lit(salt)), 256)) \
                      .withColumn("last_name", sha2(concat_ws("", "last_name", lit(salt)), 256)) \
                      .withColumn("address", sha2(concat_ws("", "address", lit(salt)), 256))

    # Save the anonymized dataset to a new file
    anonymized_df.write.csv(output_file, header=True)

    print(f"Data anonymization completed (using Spark): {output_file}")
    spark.stop()

# Main program logic
if __name__ == "__main__":    # Input and output file paths
    input_file = "sample_data.csv"
    output_file_local = "anonymized_data_local.csv"
    output_file_spark = "anonymized_data_spark.csv"

    # Determine the size of the input file
    file_size_gb = get_file_size(input_file)
    print(f"Input file size: {file_size_gb:.2f} GB")

    # Decide processing method based on file size
    if file_size_gb <= 1.0:  # Use local processing for files <= 1GB
        print("Using local processing...")
        anonymize_csv_locally(input_file, output_file_local, chunk_size=100_000)
    else:  # Use Spark for larger files
        print("Using Spark for distributed processing...")
        anonymize_csv_with_spark(input_file, output_file_spark)

