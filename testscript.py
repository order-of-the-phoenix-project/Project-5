import requests, json, time

data = {
        "/md5/thisisatest":"f830f69d23b8224b512a0dc2f5aec974",
        "/factorial/10":"3628800",
        "/fibonacci/10":"[0, 1, 1, 2, 3, 5, 8]",
        "/is-prime/233":"233 is a prime number",
        "/slack/Automated-test.":"True",
        "/kv-record/automatedtest":"True",
        "/kv-retrieve/automatedtest":"Working!"
        } 

def runtest(inp):
    test = requests.get("http://localhost:5000"+inp).json()
    assert str(test['output']) == str(data[inp])


while True:
    try:
        requests.get("http://localhost:5000/")
        print('Connected!')
        break
    except:
        print('Waiting for connection...')
        time.sleep(.5)

for x in data:
    print("Testing: "+str(x))
    runtest(x)


# def runtest(inp):
#     try:
#         test = requests.get("http://localhost:5000"+inp).json()
#         if str(test['output']) == str(data[inp]):
#             return str(inp)+" passed!"
#         else:
#             return str(inp)+" FAILED"+", expected: "+str(data[inp])+", received: "+str(test['output'])
#             failed = 1
#     except:
#         return str(inp)+" FAILED, Site error: "+str(requests.get("http://localhost:5000"+inp))
#         failed = 1

# for x in data:
#     t = runtest(x)
#     print(t)

# print(failed)