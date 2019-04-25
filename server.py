from flask import request, jsonify, json, Flask, Response
import requests, hashlib
import os 
from slackclient import SlackClient
from redis import Redis
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
    return "True"

@app.route('/md5/<string>')
def handle_md5(string):
    h = hashlib.md5(bytes(string, 'utf-8')).hexdigest()
    return jsonoutput(string, h)

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
                return jsonoutput(num, str(num) + " is not a prime number")
                #break
            else:
                return jsonoutput(num, str(num) + " is a prime number")
    except ValueError:
        return jsonoutput(num, "Input is not a positive integer")

# @app.route('/fibonacci/<num>')
# def handle_fibonacci(int(num)):
#     use = 0
#     for i in range (int(num)):
#         use = use + i
#     return str(use)

##Should be most of the slack alert API
@app.route('/slack-alert/<message>')
def handle_slack(message):
    requests.post("https://hooks.slack.com/services/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", json={"text": message})#data='\'\"text\":\"'+message+'\"\'')
    return jsonify(input = message, output = True)
    # slackurl = "https://hooks.slack.com/services/TFCTWE2SH/BGMFM5AAG/G8ENlXUDl6A68"

    # payload = {"text": str(message), "channel": "#ootpp"}
    # r = requests.post(slackurl, payload)
    # statement = "Message: " + "\"" + str(message) + "\"" + " was sucessfully posted to slack"
    # return statement
#    slack.chat.postMessage('#what channel we want to send the message to', message):
#    response = #T/F response
#    jsonoutput(message,response)

@app.route("/kv-record/<post_id>", methods=["POST","PUT"])
def create_post(post_id):
    data = request.data.decode('utf-8')
    # try:
    #     Emessage = Emessages[0]
    #     json.loads(data)
    #     return jsonify(input=post_id, output=data, error=Emessages[0])
    # except KeyError:
    #     boolean = False
    #     Emessage = Emessages[2]
    #     return jsonify(input=post_id, output=False, error=Emessages[2])
    # except ValueError:
    #     boolean = False
    #     Emessage = Emessages[1]
    #     return jsonify(input=post_id, output=False, error=Emessages[1])
    if request.method == 'PUT':
        app.redis.set(post_id, str("{\n"+"\"input\":\""+post_id+"\",\n"+"\"output\":\""+data+"\",\n"+"\"error\":\"None\"\n}"))
        return "True"
# Apparently, using jsonify does weird stuff when it puts information in Redis, and when you attempt to retrieve the data, you get something along the lines of "<Response [200]>"
    elif request.method == 'POST':
        try:
            if app.redis.exists(post_id):
                return jsonify(input=post_id, output="False", error="Unable to add pair: Key already exists.")
            else:
                app.redis.set(post_id, str("{\n"+"\"input\":\""+post_id+"\",\n"+"\"output\":\""+data+"\",\n"+"\"error\":\"None\"\n}"))
                return "True"

        except ValueError:
            return "Unable to add pair: Key already exists."
        except KeyError:
            return "Unable to add pair"


@app.route('/kv-retrieve/<id>', methods=["GET"])
def get_post(id):
    # Get from database
    try:
        post = app.redis.get(id)
        return post.decode('utf-8')
    except AttributeError:
        return "Key does not exist"

    # if post:
    #     data = json.dumps(post.decode('utf-8'))
    # else:
    #     data = False
    # return data


if __name__== '__main__':
    app.debug = False
    app.run('0.0.0.0')
