import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


config = configparser.ConfigParser()
config.read("dl.cfg")

os.environ["AWS_ACCESS_KEY_ID"] = config["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"] = config["AWS_SECRET_ACCESS_KEY"]


def create_spark_session():
    """[create_spark_session]

    Returns:
        [SparkSession]: [Spark Session]
    """
    spark = SparkSession.builder.config(
        "spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0"
    ).getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """[process_song_data]

    Args:
        spark ([SparkSession]): [Spark Session]
        input_data ([str]): [Path Input Data]
        output_data ([str]): [Path Output Data]
    """
    # get filepath to song data file
    song_data = f"{input_data}song_data/*/*/*/*.json"

    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select(
        "song_id", "title", "artist_id", "year", "duration"
    ).distinct()

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet(
        f"{output_data}songs/songs.parquet"
    )

    # extract columns to create artists table
    artists_table = df.select(
        "artist_id",
        "artist_name",
        "artist_location",
        "artist_latitude",
        "artist_longitude",
    ).distinct()

    # write artists table to parquet files
    artists_table.write.parquet(f"{output_data}artists/artists.parquet")

    df.createOrReplaceTempView("songs")


def process_log_data(spark, input_data, output_data):
    """[process_log_data]

    Args:
        spark ([SparkSession]): [Spark Session]
        input_data ([str]): [Path Input Data]
        output_data ([str]): [Path Output Data]
    """
    # get filepath to log data file
    log_data = f"{input_data}log_data/*.json"

    # read log data file
    df = spark.read.json(log_data)

    # filter by actions for song plays
    df = df.filter(df.page == "NextSong")

    # extract columns for users table
    users_table = df.select(
        "userId", "firstName", "lastName", "gender", "level"
    ).distinct()

    # write users table to parquet files
    users_table.write.parquet(f"{output_data}users/users.parquet")

    # create timestamp column from original timestamp column
    get_timestamp = F.udf(
        lambda x: datetime.fromtimestamp(int(x) / 1000), F.TimestampType()
    )
    df = df.withColumn("timestamp", get_timestamp(df.ts))

    # create datetime column from original timestamp column
    get_datetime = F.udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000)))
    df = df.withColumn("datetime", get_datetime(df.ts))

    # extract columns to create time table
    df = df.withColumn("hour", F.hour("timestamp"))
    df = df.withColumn("day", F.dayofmonth("timestamp"))
    df = df.withColumn("month", F.month("timestamp"))
    df = df.withColumn("year", F.year("timestamp"))
    df = df.withColumn("week", F.weekofyear("timestamp"))
    df = df.withColumn("weekday", F.dayofweek("timestamp"))

    time_table = df.select(
        "start_time", "hour", "day", "week", "month", "year", "weekday"
    ).distinct()

    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet(
        f"{output_data}time/time.parquet"
    )

    # read in song data to use for songplays table
    song_df = spark.sql(
        """
        SELECT DISTINCT song_id, artist_id, artist_name
        FROM songs
        """
    )

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = (
        df.join(song_df, song_df.artist_name == df.artist, "inner")
        .distinct()
        .select(
            "start_time",
            "userId",
            "level",
            "sessionId",
            "location",
            "userAgent",
            "song_id",
            "artist_id",
        )
        .withColumn("songplay_id", F.monotonically_increasing_id())
    )

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(
        f"{output_data}songplays/songplays.parquet"
    )


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://project4-udacity-datalake/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
