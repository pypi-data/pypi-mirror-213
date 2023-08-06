import requests
import json

class RabbitMonitor:

    def __init__(self, host, port, username, password, ca_file, client_cert, client_key):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ca_file = ca_file
        self.client_cert = client_cert
        self.client_key = client_key

    def get_queue_publish_rate(self, queue_name, vhost):
        url = 'https://{}:{}/api/queues/{}/{}'.format(self.host, self.port, vhost, queue_name)
        auth = (self.username, self.password)
        cert = (self.client_cert, self.client_key)
        ca_file = self.ca_file

        response = requests.get(url, auth=auth, cert=cert, verify=ca_file)
        data = json.loads(response.text)
        ds1_publish = data["message_stats"]["publish_details"]["rate"]
        return ds1_publish
