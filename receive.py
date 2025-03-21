#!/usr/bin/env python
import pika, sys, os
import json


def callback(ch, method, properties, body):
    poke_dict = json.loads(body)
    name = poke_dict["name"]
    with open(name+".json", "w") as f:
        f.write(json.dumps(poke_dict))



def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')


    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    # for binding_key in binding_keys:
    channel.queue_bind(
    exchange='topic_logs', queue=queue_name, routing_key=binding_keys[0]
    # )

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)