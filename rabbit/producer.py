#!/usr/bin/env python
import pika

print("Producer started")

# If you want to have a more secure SSL authentication, use ExternalCredentials object instead
credentials = pika.PlainCredentials(username='local_user', password='Local_pwd', erase_on_connect=True)
parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='first_vhost', credentials=credentials)

# We are using BlockingConnection adapter to start a session. It uses a procedural approach to using Pika and has most of the asynchronous expectations removed
connection = pika.BlockingConnection(parameters)
# A channel provides a wrapper for interacting with RabbitMQ
channel = connection.channel()

# Check for a queue and create it, if necessary
channel.queue_declare(queue='worker_queue')
# For the sake of simplicity, we are not declaring an exchange, so the subsequent publish call will be sent to a Default exchange that is predeclared by the broker
channel.basic_publish(exchange='', routing_key='worker_queue', body='this is the message body')
print(" [x] Sent 'this is the message body!'")

# Safely disconnect from RabbitMQ
connection.close() 
print("Producer finished")