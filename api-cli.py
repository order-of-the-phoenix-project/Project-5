"""server.py
Usage:
  server.py md5 <message>
  server.py factorial <num>
  server.py slack <message>
  server.py fibonacci <num>
  server.py prime <num>
  
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from docopt import docopt
import requests

def sendinfo(type, info):
    return requests.get("http://localhost:5000/"+type+"/"+info).json()['output']


def run():
    args = docopt(__doc__, version="0.1.0")

    if args['md5']:
        print(sendinfo('md5', args['<message>']))
    if args['factorial']:
        print(sendinfo('factorial', args['<num>']))
    if args['slack']:
        print(sendinfo('slack', args['<message>']))
    if args['fibonacci']:
        print(sendinfo('fibonacci', args['<num>']))
    if args['prime']:
        print(sendinfo('is-prime', args['<num>']))

if __name__ == "__main__":
    run()