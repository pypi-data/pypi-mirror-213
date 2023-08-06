sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.simplerabbit.receiver import RabbitReceiver

def on_message(msg_type, msg):
    print('Receive msg_type={} msg={}'.format(msg_type, msg))


s = RabbitReceiver('localhost', 5672, 'guest', 'guest', 'ATOM')
s.connect()
s.set_message_callback(on_message)

s.subscribe('test_simplerabbit', 'direct_exchange', 'test')
s.start_consuming()
