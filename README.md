# HTTP_Web_Service
This project originated from CSE138 Distributed System course at University of California Santa Cruz under the assistance of Prof. Liting Hu. 

# HTTP Web Service
- Differentiates between requests with different HTTP verbs (GET/POST) and URI paths (/hello, /hello/<name>, and /test).


# HTTP Interface
## assignment1.py
### /hello
- Accepts a **GET** request with no parameter.
- Return the JSON response body {"message": "world"} with status code 200.

Example:

`$ curl--request GET--header "Content-Type: application/json"--write-out "\n%{http_code}\n" http://localhost:8090/hello`
```
{"message":"world"}
200
```

- If receiving a POST request with or without any response body, it returns the error message {"Method Not Allowed"} with status code 405.

Example:

`$ curl--request POST--write-out "\n%{http_code}\n" http://localhost:8090/hello/slug`
```
{"message":"Hi, slug."}
200
```

### /hello/\<name\>
- Accepts a **POST** request with the path-parameter "name".
- Return the JSON response body {"message":"Hi, \<name\>."} with status code 200.

Example:

`$ curl--request POST--write-out "\n%{http_code}\n" http://localhost:8090/hello`
```
Method Not Allowed
405
```

- If receiving a GET request, it returns the error message {"Method Not Allowed"} with status code 405.

### /test
- Accepts a **GET** request with no parameter.
- Returns the JSON response body {"message":"test is successful"} with status code 200

Example:

`$ curl--request GET--header "Content-Type: application/json"--write-out "\n%{http_code}\n" http://localhost:8090/test`
```
{"message":"test is successful"}
200
```

- Accepts a **POST** request with a msg query parameter.
- Returns the JSON response body {"message":"\<msg\">} with status code 200 where \<msg\> is the string passed to the msg query parameter.

Example:

`curl--request POST--header "Content-Type: application/json"--write-out "\n%{http_code}\n" "http://localhost:8090/test?msg=foo`
```
{"message":"foo"}
200
```

- If receiving a POST request without any msg query parameter, it returns the error message {"Bad Request"} with status code 400.
- If receiving an unknown query parameter, it returns the error message {"Bad Request"} with status code 400.


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
