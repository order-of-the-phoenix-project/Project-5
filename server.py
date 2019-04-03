from flask import request, jsonify, json, Flask
import requests
import os 
from slackclient import SlackClient
from redis import redis
import json


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
        
@app.route('/')
def index():
    return "it works"

# @app.route('/md5/<string>')
# def handle_md5(string):
#     h = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
#     return h

@app.route('/factorial/<num>')
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

@app.route('/fibonacci/<num>')
def fibonacci(num):
    a = 0
    b = 1
    fibo = [a]
    while b <= int(num):
        fibo.append(b)
        a, b = b, a+b
    return jsonoutput(int(num), fibo)    

@app.route('/is-prime/<number>')
def handle_prime(number):
    try:    
    num = int(number)
        for i in range(2,num):
            if (num % i) == 0:
                return jsonoutput(str(num) + " is not a prime number")
                break
            else:
                return jsonoutput(str(num) + " is a prime number")
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

@app.route('/posts/<post_id>', methods=["GET"])
def get_post(post_id):

    post = app.redis.get(post_id).decode('utf-8')
    return json.dumps(post)


@app.route("/posts/<post_id>", methods["POST"])
def create_post(post_id):

    data = request.data.decode("utf-8")
    data = json.loads(data)

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


if _name_= '_main_':
app.debug = True
app.run('0.0.0.0')