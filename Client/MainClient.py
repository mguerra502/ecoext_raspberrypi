import sys
from PoS import PoS
import json

def MainClient():
    with open('{}'.format(sys.argv[3])) as f:
        message = json.load(f)
    
    clientPoS = PoS(sys.argv[1], int(sys.argv[2]), message)
    clientPoS.sendMessageToServer()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: {} <host> <port> <message>".format(sys.argv[0]))
        sys.exit(1)

    MainClient()