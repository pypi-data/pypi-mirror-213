import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.simplerabbit.monitor import RabbitMonitor

if len(sys.argv) != 8:
    print('Arguments : <queue_name> <vhost> <username> <password> <ca_cert> <client_cert> <client_key>')
    print('For example : python3 {} {} {} {} {} {} {} {}'.format(
            sys.argv[0]
            , 'ds_queue_DS1'
            , 'ATOM'
            , 'ATOM_RABBIT_ADMIN'
            , '<password>'
            , '/usr/local/atom/cfg/rabbitmq_ca_cert.pem'
            , '/usr/local/atom/cfg/rabbitmq_client_cert.pem'
            , '/usr/local/atom/cfg/rabbitmq_client_key.pem'
        ))
else:
    queue_name = sys.argv[1]
    vhost = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    ca_cert = sys.argv[5]
    client_cert = sys.argv[6]
    client_key = sys.argv[7]
    monitor = RabbitMonitor('localhost', 15671, username, password, ca_cert, client_cert, client_key)
    while True:
        rate = monitor.get_queue_publish_rate(queue_name, vhost)
        print('Publish rate : {}'.format(rate))
        time.sleep(3)
