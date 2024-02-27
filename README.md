This project originated from CSE138 Distributed System course at University of California Santa Cruz under the assistance of Prof. Liting Hu. 

# HTTP Interface
## assignment1.py
### HTTP Service
- **Service Creation**: Implement an HTTP web service that recognizes different HTTP verbs and URI paths.
- **Containerization**: Package the service in a container image listening on port 8090, described by a Dockerfile or Containerfile.

### Endpoints and Behaviors
### /hello
- GET: Returns {"message":"world"} with status 200.
- POST: Responds with status 405 (Method Not Allowed).

Example:
```python
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return jsonify({"message": "world"}), 200
    else:  # POST request
        abort(405)  # Method Not Allowed
```

### /hello/\<name\>
- POST: Accepts a name as a path parameter, returning {"message":"Hi, \<name\>."} with status 200.
- GET: Responds with status 405.

Example:
```
@app.route('/hello/\<name\>', methods=['GET', 'POST'])
def hello_name(name):
    if request.method == 'POST':
        return jsonify({"message": f"Hi, {name}."}), 200
    else:  # GET request
        abort(405)  # Method Not Allowed
```

### /test
- GET: Returns {"message":"test is successful"} with status 200.
- POST with msg query parameter: Returns {"message":"\<msg\>"} with status 200.
- POST without msg query parameter: Responds with status 400 (Bad Request).

Example:
```python
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
```

## assignment2.py
### Key Features
#### In-Memory Store
- The key-value data is stored in memory using a Python dictionary, allowing for quick access and modifications.

#### CRUD Operations
- Create/Update (PUT): Adds a new key-value pair to the store or updates the value for an existing key. The service handles this through a PUT request to the /kvs/\<key\> endpoint, where <key> is the key to be added or updated. The value must be included in the JSON body of the request.

Example:
```python
@app.route('/kvs/<key>', methods=['PUT'])
def handle_key(key):
    # Code to add or update a key-value pair
    data = request.get_json()
    value = data['value']
    kv_store[key] = value
    return jsonify({"result": "created"}), 201
```
- READ (GET): Retrieves the value associated with a given key. This is accomplished by making a GET request to /kvs/\<key\>. If the key exists, its value is returned; otherwise, a 404 error is generated.

Example:
```python
@app.route('/kvs/<key>', methods=['GET'])
def handle_key(key):
    # Code to retrieve the value for a key
    if key in kv_store:
        return jsonify({"result": "found", "value": kv_store[key]}), 200
    else:
        return jsonify({"error": "Key does not exist"}), 404
```
- Delete (DELETE): Removes a key-value pair from the store. This operation is performed by sending a DELETE request to /kvs/\<key\>. If the key is found, it is removed, and a success response is returned; if not, a 404 error is returned.

Example:
```python
@app.route('/kvs/<key>', methods=['DELETE'])
def handle_key(key):
    # Code to delete a key-value pair
    if key in kv_store:
        del kv_store[key]
        return jsonify({"result": "deleted"}), 200
    else:
        return jsonify({"error": "Key does not exist"}), 404
```

#### Error Handling
- The service includes robust error handling, ensuring that clients receive meaningful error messages and HTTP status codes for various error conditions, such as:
  - Key length exceeds 50 characters: Returns a 400 Bad Request error.
  - PUT request without a value specified: Returns a 400 Bad Request error.
  - Attempt to access or delete a non-existent key: Returns a 404 Not Found error.

#### Forwarding Mode
- When the service is configured with a forwarding address (via the FORWARDING_ADDRESS environment variable), it acts as a proxy, forwarding all incoming requests to another instance of the service. This feature allows the service to be part of a distributed system where requests can be redirected as needed for load balancing or fault tolerance.

Example:
```
@app.route('/kvs/<key>', methods=['GET','PUT','DELETE'])
def forward_key_request(key):
    # Code to forward the request to another service instance
    url = f"http://{forwarding_address}/kvs/{key}"
    response = requests.get(url) # Example for GET
    return jsonify(response.json()), response.status_code
```




### Acknowdgegets:

TA: Cheng-Wei Ching

Tutor: Albert Lee

### Team Contributors:

Jun Hayashida

Justin Morales

Tyler Fong

### Citations:
- "What even is a container: namespaces and cgroups": https://jvns.ca/blog/2016/10/10/what-even-is-a-container/
- "RESTful Web Service": http://www.restfulwebapis.org/rws.html
- "Basic Flask operation for Python": https://www.youtube.com/watch?v=Z1RJmh_OqeA
- "key-value store/pair: https://hazelcast.com/glossary/key-value-store/
- "jsonify()": nhttps://www.geeksforgeeks.org/use-jsonify-instead-of-json-dumps-in-flask/#
- "Empty reply from server": moby/moby#2522
- https://www.geeksforgeeks.org/put-method-python-requests/
- https://stackoverflow.com/questions/23144622/how-to-set-http-request-timeout-in-python-flask
- https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
