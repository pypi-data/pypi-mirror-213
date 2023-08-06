import ssl
import pika

class RabBase:
    def __init__(self, host='localhost', port='5672', username=None, password=None, virtual_host='/', ca_cert='', client_cert='', client_key=''):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.client_key = client_key
        self.connection = None
        self.channel = None

    def connect(self):
        if self.ca_cert and self.client_cert and self.client_key:
            self._connect_ssl()
        else:
            self._connect_insecured()
        self.channel = self.connection.channel()

    def _connect_ssl(self):
        print('ca_cert = {}'.format(self.ca_cert))
        print('client_cert = {}'.format(self.client_cert))
        print('client_key = {}'.format(self.client_key))
        ssl_context = ssl.create_default_context(cafile=self.ca_cert)
        ssl_context.load_cert_chain(self.client_cert, self.client_key)

        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials,
            #ssl_options=pika.SSLOptions(ssl_context, 'www.test.edatom.dk'),
            ssl_options=pika.SSLOptions(ssl_context),
        )
        self.connection = pika.BlockingConnection(parameters)

    def _connect_insecured(self):
        credentials = pika.PlainCredentials(self.username,
                                            self.password) if self.username and self.password else None
        parameters = pika.ConnectionParameters(host=self.host, port=self.port, virtual_host=self.virtual_host,
                                               credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)

