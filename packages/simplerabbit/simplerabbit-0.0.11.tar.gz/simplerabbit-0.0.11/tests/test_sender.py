import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.simplerabbit.monitor import RabbitSender

s = RabbitSender('localhost',5672, 'guest', 'guest', 'ATOM')
s.connect()
while True:
    s.send_message('direct_exchange', 'test', 10, 'Hello World')
    print('Sent one message')
    time.sleep(5)
