# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import from_json,udf,col
from pyspark.sql.types import StructType, StructField, StringType, LongType, IntegerType, BooleanType, FloatType
from credibility import credibility,textCredibility,userCredibility,socialCredibility
from kafka import KafkaProducer
from confluent_kafka import Consumer
import json
import time
#import pymongo



def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

props = read_ccloud_config("client.properties")
props["group.id"] = "python-group-1"
props["auto.offset.reset"] = "earliest"



conf = SparkConf()
conf.setAppName("TwitterStream")
conf.set("spark.streaming.uninterruptibleProgressTimeout", "0")
#conf.set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.13:10.1.1")


# Configuración de Spark y Kafka
spark = SparkSession.builder.config(conf=conf).getOrCreate()

schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("username", StringType(), True),
    StructField("tweet_id",StringType(),True),
    StructField("text", StringType(), True),
    StructField("created_at", StringType(), True),
    StructField("verified", BooleanType(), True),
    StructField("followers_count", IntegerType(), True),
    StructField("following_count", IntegerType(), True),
    StructField("retweet_count", IntegerType(), True),
    StructField("like_count", IntegerType(), True),
    StructField("lang", StringType(), True)
])

text_credibility_udf = udf(lambda text,lang:
                        textCredibility(text,lang), FloatType())

user_credibility_udf = udf(lambda verified, created_at:
                       userCredibility(verified,created_at),FloatType())

social_credibility_udf = udf(lambda followers_count,following_count:
                        socialCredibility(followers_count,following_count),FloatType())

global_credibility_udf = udf(lambda text_credibility,social_credibility,user_credibility:
                        credibility(text_credibility,social_credibility,user_credibility), FloatType())

kafka_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", props["bootstrap.servers"]) \
    .option("subscribe", "twitter") \
    .option("group.id",props["group.id"])\
    .option("startingOffsets", props["auto.offset.reset"] ) \
    .option("kafka.security.protocol",props["security.protocol"])\
    .option("kafka.sasl.jaas.config", f"org.apache.kafka.common.security.plain.PlainLoginModule required username=\"{props['sasl.username']}\" password=\"{props['sasl.password']}\";")\
    .option("kafka.sasl.mechanism",props["sasl.mechanisms"])\
    .option("auto.offset.reset",props["auto.offset.reset"])\
    .load() \
    .selectExpr("CAST(value AS STRING)")\
    .select(from_json(col("value"), schema).alias("tweet"))\
    .select(col("tweet.user_id").alias("user_id"),
            col("tweet.username").alias("username"),
            col("tweet.tweet_id").alias("tweet_id"),
            col("tweet.text").alias("text"),
            col("tweet.created_at").alias("created_at"),
            col("tweet.verified").alias("verified"),
            col("tweet.followers_count").alias("followers_count"),
            col("tweet.following_count").alias("following_count"),
            col("tweet.retweet_count").alias("retweet_count"),
            col("tweet.like_count").alias("like_count"),
            col("tweet.lang").alias("lang"))\
    .withColumn("text_credibility", text_credibility_udf("text", "lang"))\
    .withColumn("social_credibility",social_credibility_udf("followers_count","following_count"))\
    .withColumn("user_credibility",user_credibility_udf("verified","created_at"))\
    .withColumn("global_credibility",global_credibility_udf("text_credibility","social_credibility","user_credibility"))

query = kafka_stream \
    .selectExpr("to_json(struct(*)) AS value") \
    .writeStream \
    .format("kafka") \
    .option("checkpointLocation", "/mnt/c/Users/Xabier/source/repos/T-Creo-Chrome/checkpoint") \
    .option("forceDeleteTempCheckpointLocation", "true") \
    .option("kafka.bootstrap.servers", props["bootstrap.servers"]) \
    .option("topic", "chrome") \
    .option("startingOffsets", props["auto.offset.reset"]) \
    .option("kafka.security.protocol", props["security.protocol"]) \
    .option("kafka.sasl.jaas.config", f"org.apache.kafka.common.security.plain.PlainLoginModule required username=\"{props['sasl.username']}\" password=\"{props['sasl.password']}\";") \
    .option("kafka.sasl.mechanism", props["sasl.mechanisms"]) \
    .option("auto.offset.reset", props["auto.offset.reset"]) \
    .start().awaitTermination()


#query = kafka_stream \
#   .writeStream \
#    .format('mongodb') \
#    .option("checkpointLocation", "/mnt/c/Users/Xabier/source/repos/T-Creo-Chrome/checkpoint")\
#    .option("forceDeleteTempCheckpointLocation", "true")\
#    .option("spark.mongodb.connection.uri", "mongodb+srv://xabier:ENXKLSNvrWqd3dYJ@cluster0.rmdseqj.mongodb.net/?retryWrites=true&w=majority") \
#    .option("spark.mongodb.database", "Test") \
#    .option("spark.mongodb.collection", "StreamData") \
#    .outputMode("append") \
#    .start().awaitTermination()