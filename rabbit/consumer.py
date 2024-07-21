#!/usr/bin/env python
import pika, sys, os

# Here we define the main script that will be executed forever until a keyboard interrupt exception is received
def main():
    credentials = pika.PlainCredentials('local_user', 'Local_pwd')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='first_vhost', credentials=credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='worker_queue')
    
    # Since RabbitMQ works asynchronously, every time you receive a message, a callback function is called. We will simply print the message body to the terminal 
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    # Consume a message from a queue. The auto_ack option simplifies our example, as we do not need to send back an acknowledgement query to RabbitMQ which we would normally want in production
    channel.basic_consume(queue='worker_queue', on_message_callback=callback, auto_ack=False, consumer_tag="user")
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    # Start listening for messages to consume
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)