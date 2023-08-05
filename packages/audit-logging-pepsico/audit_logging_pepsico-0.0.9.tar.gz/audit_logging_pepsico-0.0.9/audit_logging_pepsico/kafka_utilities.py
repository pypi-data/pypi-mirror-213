import sys
import json
from confluent_kafka import Producer
from confluent_kafka import Consumer
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions,
                               ClusterTimeoutOptions,
                               QueryOptions,
                               WaitUntilReadyOptions)
from couchbase.auth import PasswordAuthenticator
from datetime import timedelta
from couchbase.diagnostics import ServiceType
import base64
import time


def connect_kafka_producer(kafka_producer_config, logger):
    producer = None
    err = ""
    try:
        producer = Producer(kafka_producer_config)
    except Exception as ex:
        logger.error('Exception while connecting Kafka')
        logger.error(str(ex))
        err = str(ex)
    finally:
        if err == "":
            return True, producer
        else:
            return False, err


def connect_kafka_consumer(kafka_consumer_config, logger):
    consumer = None
    err = ""
    try:
        consumer = Consumer(kafka_consumer_config)
    except Exception as ex:
        logger.error('Exception while connecting Kafka')
        logger.error(str(ex))
        err = str(ex)
    finally:
        if err == "":
            return True, consumer
        else:
            return False, err


def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}: value = {value:12}".format(
            topic=msg.topic(), value=msg.value().decode('utf-8')))


def kafka_produce_events(audit_log_str: str, kafka_producer, kafka_topic, logger):
    try:
        kafka_producer.produce(kafka_topic, audit_log_str, callback=delivery_callback)
        kafka_producer.poll(10000)
        kafka_producer.flush()
        return True, "Kafka Audit logs produced successfully"
    except Exception as err:
        logger.info("Kafka Producer Error: " + str(err))
        return False, "Exception: " + str(err)


def couchbase_insert_logs(couchbase_config, doc, logger):
    try:
        key = doc["componentName"] + " " + doc["createdDate"]
        conn_str = couchbase_config["conn_str"]
        cb_username = couchbase_config["cb_username"]
        cb_password = couchbase_config["cb_password"]
        cb_password = base64.b64decode(cb_password.encode('utf-8')).decode('utf-8')
        bucket_name = couchbase_config["bucket_name"]
        auth = PasswordAuthenticator(cb_username, cb_password)
        timeout_opts = ClusterTimeoutOptions(connect_timeout=timedelta(seconds=20),
                                             kv_timeout=timedelta(seconds=20))
        options = ClusterOptions(auth, timeout_options=timeout_opts)
        # options = ClusterOptions(auth)
        cluster = Cluster.connect(conn_str, options)
        cluster.wait_until_ready(timedelta(seconds=10),
                                 WaitUntilReadyOptions(service_types=[ServiceType.KeyValue, ServiceType.Query]))
        logger.info("Cluster ==== \n" + str(cluster))
        bucket = cluster.bucket(bucket_name)
        logger.info("Bucket ==== " + str(bucket))
        coll = bucket.default_collection()
        logger.info("Colle === " + str(coll))
        res = coll.upsert(key, doc)
        logger.info("upsert res === " + str(res.cas))
        res = coll.get(key)
        logger.info("res === " + str(res.content_as[str]))
        return True, res
    except Exception as err:
        logger.error("Exception in couchbase: " + str(err))
        return False, "Exception: " + str(err)


def kafka_consume_logs(kafka_consumer_config, kafka_topic, couchbase_config, logger, duration):
    kafka_consumer_connect_status, kafka_consumer = connect_kafka_consumer(kafka_consumer_config, logger)
    if kafka_consumer_connect_status:
        kafka_consumer.subscribe([kafka_topic])
        try:
            t_end = time.time() + duration
            while time.time() < t_end:
                msg = kafka_consumer.poll(1.0)
                logger.info("Consumer Message: " + str(msg))
                if msg is not None and msg.error() is None:
                    logger.info("Kafka Topic: " + str(msg.topic()))
                    logger.info("Kafka Message Value: " + str(json.loads(msg.value())))
                    msg_value = json.loads(msg.value())
                    couchbase_resp_status, coucbase_resp_msg = couchbase_insert_logs(couchbase_config, msg_value, logger)
                    if couchbase_resp_status:
                        logger.info("Kafka Log is consumed and inserted in Couchbase")
                    else:
                        logger.error(coucbase_resp_msg)
                        return False, coucbase_resp_msg
                elif msg is not None and msg.error() is not None:
                    logger.error("Kafka Consumer Error: " + str(msg.error()))
                    return False, "Error: " + str(msg.error())
            return True, "Kafka Audit Logs Consumed Successfully"
        except KeyboardInterrupt:
            kafka_consumer.close()
            return True, "Kafka Consumer Stopped Successfully"
        except Exception as err:
            logger.error("Kafka Consumer Error: " + str(err))
            return False, "Exception: " + str(err)
        finally:
            kafka_consumer.close()
    else:
        return False, kafka_consumer
