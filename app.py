import json
import os
import time

from google.cloud import pubsub_v1


PUB_SUB_PROJECT = os.environ.get('PUB_SUB_PROJECT')
PUB_SUB_TOPIC = os.environ.get('PUB_SUB_TOPIC')
PUB_SUB_SUBSCRIPTION = os.environ.get('PUB_SUB_SUBSCRIPTION')
TIMEOUT = 15.0


def push_message(message, topic, project):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    data = json.dumps(message).encode("utf-8")
    publisher.publish(topic_path, data=data)
    print("[+] Message pushed to topic: {}".format(topic_path))
    return


def process_message(message):
    print("[i] Received message: {}".format(message))
    data = json.loads(message.data)
    delay = data.get("delay")
    
    if delay is not None and delay > time.time():
        print("[-] Message delayed: {}".format(delay))
    else:
        print("[+] Data processed: {}".format(data))
        print("[+] Delay processed: {}".format(delay))
        message.ack()


def consume_message(project, subscription, callback, period):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)
    print("[i] Listening for message on: {}".format(subscription_path))
    streaming_pull = subscriber.subscribe(subscription_path, callback=callback)

    with subscriber:
        try:
            streaming_pull.result(timeout=period)
        except TimeoutError:
            streaming_pull.cancel()


def main():
    if PUB_SUB_PROJECT is None:
        raise Exception("Error: Must export PUB_SUB_PROJECT")
    if PUB_SUB_TOPIC is None:
        raise Exception("Error: Must export PUB_SUB_TOPIC")
    if PUB_SUB_SUBSCRIPTION is None:
        raise Exception("Error: Must export PUB_SUB_SUBSCRIPTION")
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
        raise Exception("Error: Must export GOOGLE_APPLICATION_CREDENTIALS")

    current_epoch = time.time()

    message = {"message" : "Payload data", "delay": current_epoch + 10, "timestamp": time.time()}
    push_message(message, PUB_SUB_TOPIC, PUB_SUB_PROJECT)

    message = {"message" : "Payload data", "delay": current_epoch + 10, "timestamp": time.time()}
    push_message(message, PUB_SUB_TOPIC, PUB_SUB_PROJECT)

    message = {"message" : "Payload data", "delay": current_epoch + 10, "timestamp": time.time()}
    push_message(message, PUB_SUB_TOPIC, PUB_SUB_PROJECT)

    message = {"message" : "Payload data", "delay": current_epoch + 10, "timestamp": time.time()}
    push_message(message, PUB_SUB_TOPIC, PUB_SUB_PROJECT)

    message = {"message" : "Payload data", "delay": current_epoch + 10, "timestamp": time.time()}
    push_message(message, PUB_SUB_TOPIC, PUB_SUB_PROJECT)
    
    while(True):
        print("===================================")
        consume_message(PUB_SUB_PROJECT, PUB_SUB_SUBSCRIPTION, process_message, TIMEOUT)
    

if __name__ == ("__main__"):
    main()
