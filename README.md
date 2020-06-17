# Kafka_Twitter
This is a distributed streaming application that reads tweets from twitter using Python, and pipes it to Kafka streams. Jobs are run using Zookeeper and kafka. 

# RUNNING THE CODE
. First run your Kafka and zookeeper in your terminal after installation. 
  --
   Here is the doc file I have created which will help you out
    https://docs.google.com/document/d/1e_q4wi2NsARwHn2Ws-JuJVe1SscwudaMRE6-0yCFWMs/edit
    
. Run tweet_kafka.py and check.py together. 
  --
   tweet_kafka(streaming data from twitter and sending by producer to kafka)
   
   
   check_kafka(storing all the crucial data coming to consumer in csv file as .. tweets.csv) 

. to deliver the stream to csv:
 and there is csv file tweets.csv which is storing data from consumer so that you can further use for analysis purpose
 

###########################################
*** Note ***

this procedure assumes a topic named twitterstream exists in kafka to produce the data to.
if you need to create a topic use the following code :

>> bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitterstream

check what topics you have with:
>> bin/kafka-topics.sh --list --zookeeper localhost:2181

to check if data is in fact landing in kafka:
>> bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic twitterstream --from-beginning
 


  

