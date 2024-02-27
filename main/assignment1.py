# Jun Hayashida
# assignment1.py
# Create an HTTP web service that differentiates between requests 
# with different HTTP verbs (GET and POST)
# and URI paths (/hello, /hello/<name>, and /test).

from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# /hello Endpoint:
# - Accepts GET request and returns {"message": "world"} with a 200 status code.
# - For POST requests, returns a 405 status code.
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return jsonify({"message": "world"}), 200
    else:  # POST request
        abort(405)  # Method Not Allowed

# /hello/<name> Endpoint:
# - Accepts POST request with the path-parameter "name".
#   Returns {"message":"Hi, <name>."} with a 200 status code.
# - For GET requests, returns a 405 status code.
@app.route('/hello/<name>', methods=['GET', 'POST'])
def hello_name(name):
    if request.method == 'POST':
        return jsonify({"message": f"Hi, {name}."}), 200
    else:  # GET request
        abort(405)  # Method Not Allowed


# /test Endpoint:
# - Accepts GET request with no query parameters and returns 
#   {"message":"test is successful"} with a 200 status code.
# - Accepts POST request with a 'msg' query parameter.
#   Returns {"message":"<msg>"} with a 200 status code if 'msg' is provided,
#   else returns a 400 status code.
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        return jsonify({"message": "test is successful"}), 200
    elif request.method == 'POST':
        msg = request.args.get('msg')
        if msg:
            return jsonify({"message": msg}), 200
        else:
            abort(400)  # Bad Request

# Main entry point, runs the app on host 0.0.0.0 and port 8090
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8090)