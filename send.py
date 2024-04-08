import pika
import requests
import random
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

poke_id = random.randint(1,150)
# poke_id = 1

poke_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}")
poke_json = poke_response.json()

message = {}
# message["name"] = poke_json["name"]
message["types"] = poke_json["types"]

for type in poke_json["types"]:
    channel.basic_publish(
    exchange='topic_logs', routing_key=type["type"]["name"], body=json.dumps(poke_json))
    print(f"type emmited: {type['type']['name']}")

print(f" [x] Sent pokemon of the moment")

connection.close()