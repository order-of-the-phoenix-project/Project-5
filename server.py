"""server.py

Usage:
  server.py factorial <num>
  server.py slack <message>
  server.py fibonacci <num>
  server.py prime <num>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from flask import request, jsonify, json, Flask
import requests
import os 
from slackclient import SlackClient
from redis import Redis
import json
from docopt import docopt




app = Flask(__name__)
app.redis = Redis(host="redis", port=6379)
# NOTE: error handling for letters entered when number expected:
# try:
#     float(element)
# except ValueError:
#     print "Not a float"

# def factorial(num):
#     total = num
#     for i in range(1, num - 1):
#         num -= 1
#         total = total * (num)
#     return total 

def jsonoutput(inp, outp):
    return jsonify(input=inp, output=outp) 

def handle_factorial(num):
    try:
        use = int(num)
        total = int(num)
        for i in range(1, int(num) - 1):
            use -= 1
            total = total * use
        return jsonoutput(int(num), total)
        #return str(total)
    except ValueError:
        return jsonoutput(num, "Input is not a positive integer")

def handle_fibonacci(num):
    a = 0
    b = 1
    fibo = [a]
    while b <= int(num):
        fibo.append(b)
        a, b = b, a+b
    return jsonoutput(int(num), fibo)

@app.route('/')
    
def index():
    return "it works"

    # @app.route('/md5/<string>')
    # def handle_md5(string):
    #     h = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
    #     return h



@app.route('/factorial/<num>')
def factorial(num):
    handle_factorial(num)

@app.route('/fibonacci/<num>')
def fibonacci(num):
    handle_fibonacci(num)  

@app.route('/is-prime/<number>')
def handle_prime(number):
    try:    
        num = int(number)
        for i in range(2,num):
            if (num % i) == 0:
                return jsonoutput(number, str(num) + " is not a prime number")
                break
            else:
                return jsonoutput(number, str(num) + " is a prime number")
    except ValueError:
        return jsonoutput(num, "Input is not a positive integer")

# @app.route('/fibonacci/<num>')
# def handle_fibonacci(int(num)):
#     use = 0
#     for i in range (int(num)):
#         use = use + i
#     return str(use)

##Should be most of the slack alert API
@app.route('/slack/<message>')
def handle_slack(message):
    slack_token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(slack_token)

    sc.api_call(
    "chat.postMessage",
    channel="ootpp",
    text=str(message)
)
    return jsonify(message = True)
    # slackurl = "https://hooks.slack.com/services/TFCTWE2SH/BGMFM5AAG/G8ENlXUDl6A68"

    # payload = {"text": str(message), "channel": "#ootpp"}
    # r = requests.post(slackurl, payload)
    # statement = "Message: " + "\"" + str(message) + "\"" + " was sucessfully posted to slack"
    # return statement
#    slack.chat.postMessage('#what channel we want to send the message to', message):
#    response = #T/F response
#    jsonoutput(message,response)

@app.route("/kv-record/<post_id>", methods=["POST"])
def create_post(post_id):
    data = request.data.decode("utf-8")
    data = json.loads(data)
    post = app.redis.get(id)
    app.redis.set(post_id, post)
    return "True"


@app.route('/kv-retrieve/<id>', methods=["GET"])
def get_post(id):
        # Get from database
        post = app.redis.get(id)
        if post:
            data = json.dumps(post.decode('utf-8'))
        else:
            data = json.dumps(())
        return data

def create_app():
    app = Flask(__name__)

    with app.app_context():
        run()

    return app

def run():
    cli = False
    print(cli)
    args = docopt(__doc__, version="0.1.0")
    print(args)
    if args['factorial']:
        ans = handle_factorial(args['<num>'])
        print(ans.data)
        cli = True
    print(cli)
    if args['slack']:
        ans = handle_slack(args['<message>'])
        print(ans.data)
        cli = True
    
    if args['fibonacci']:
        ans = handle_fibonacci(args['<num>'])
        print(ans.data)
        cli = True

    if args['prime']:
        ans = handle_prime('<num>')
        print(ans.data)
        cli = True
    
    # if args['kvget']:
    #     ans = get_post()
    #     print(ans.data)

    # if args['kvpost']:
    #     ans = create_post()
    #     print(ans.data)
   
    if ((__name__== '__main__') and (cli == False)):
        app.debug = False
        app.run('0.0.0.0')

    

if __name__ == '__main__':
        create_app()
    

