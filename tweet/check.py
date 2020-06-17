import csv

from kafka import KafkaConsumer

from tweet.tweet_kafka import mytopic


def save_data():
    consumer = KafkaConsumer(mytopic, bootstrap_servers='localhost:9092')
    for message in consumer:
        print(message)
        with open(f'csv/tweets.csv', "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(message)

save_data()
