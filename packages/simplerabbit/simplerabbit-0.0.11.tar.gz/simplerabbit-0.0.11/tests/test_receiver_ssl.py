import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.simplerabbit.receiver import RabbitReceiver

def on_message(msg_type, msg):
    print('Receive msg_type={} msg={}'.format(msg_type, msg))


ca_cert = sys.argv[1]
client_cert = sys.argv[2]
client_key = sys.argv[3]
s = RabbitReceiver('localhost',5671, 'guest', 'guest', 'ATOM', ca_cert=ca_cert, client_cert=client_cert, client_key=client_key)
s.connect()
s.set_message_callback(on_message)

s.subscribe('test_simplerabbit', 'direct_exchange', 'test')
s.start_consuming()
