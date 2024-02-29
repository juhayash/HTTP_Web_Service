This project originated from CSE138 Distributed System course at University of California Santa Cruz under the assistance of Prof. Liting Hu. 

# HTTP Interface
## HTTP_Service.py
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


## InMemory_Store.py
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

## Replicated_KeyValue_Store.py
### Key Features
#### Replicated Key-Value Store Design
- **Replication**: Each instance of your key-value store replicates its data across all other instances to ensure fault tolerance and data availability.
- **Fault Tolerance**: The system remains available even if one or more replicas fail.
- **Causal Consistency**: Updates respect the causal order of events, ensuring that all replicas maintain a consistent view of the data that respects the sequence of operations.

#### Communication Among Replicas
- Replicas communicate any state changes (additions, deletions of keys) to each other, ensuring all replicas have the same data.
- When a replica goes down, its data is not lost since it's replicated across other running instances.
- Replicas use causal metadata to provide a causally consistent view to the clients. This metadata is exchanged between clients and replicas to ensure clients always see a consistent state of the data.

#### API Design
- View Management: Handles adding or removing replicas in the system.
    - PUT /view: Add a new replica. If the replica already exists, the operation is idempotent.
    - GET /view: Retrieve the current list of replicas.
    - DELETE /view: Remove an existing replica from the cluster.

- Data Management with causal consistency.
    - PUT /kvs/\<key\>: Add or update a key-value pair, including causal metadata for consistency.
    - GET /kvs/\<key\>: Retrieve the value for a key, respecting causal dependencies.
    - DELETE /kvs/\<key\>: Remove a key-value pair, ensuring causal consistency.

#### Ensuring Safety and Liveness
- **Causal Consistency (Safety)**
    - Enforces an agreement on the order of causally related writes. This is crucial for maintaining a consistent state across replicas that respect the sequence of operations.
    - Implementing causal consistency involves managing metadata that captures the history or sequence of updates, allowing the system to determine the causal relationships between operations.

- **Eventual Consistency (Liveness)**
    - Ensures that if no new writes are made, all replicas will eventually reach the same state.
    - This property is achieved through continuous synchronization of updates among replicas, ensuring that any temporary discrepancies between replicas are resolved over time.

#### Technical Considerations
- **Detecting Replica Failures**
    - Implement heartbeats or periodic checks among replicas to detect failures.
    - Upon detecting a failure, the replica is removed from the view, and other replicas are informed to update their views accordingly.

- **Adding a New Replica:**
    - The new replica broadcasts its presence.
    - Existing replicas add the new replica to their view.
    - The new replica fetches the current state of the key-value store from an existing replica to initialize its local store.

- **Metadata Management for Causal Consistency:**
    - Use vector clocks or similar mechanisms to track causal dependencies among operations.
    - Ensure that operations are processed in a way that respects these dependencies, maintaining the causal consistency of the system.

- **Conflict Resolution**
    - In cases where concurrent updates occur, define a conflict resolution strategy, such as last-write-wins or merging updates based on timestamps or logical clocks.


### Acknowdgegets:

TA: Cheng-Wei Ching

Tutor: Albert Lee

### Team Contributors:

### Jun Hayashida:
- **HTTP_Service.py**
    - Developed an HTTP web service using Flask to differentiate between requests using various HTTP verbs (GET and POST) and URI paths (/hello, /hello/<name>, and /test), showcasing the ability to handle dynamic web service requests efficiently.
    - Implemented logic to return appropriate responses based on the HTTP method and URI path, including error handling for unsupported methods, to demonstrate an understanding of RESTful principles and HTTP status codes.
    - Conducted thorough testing to ensure the service accurately processes requests and returns the expected outcomes, contributing to the system's reliability and robustness.
    - Optimized the code structure for improved readability and maintainability, facilitating easier future enhancements and understanding for other developers.

- **InMemory_Store.py**
    - Implemented a Flask-based API to manage an in-memory keyvalue store, which supports 'PUT', 'GET', and 'DELETE' HTTP methods.
    - Added input validation, error handling, and logic to create, update, or delete key-value pairs with corresponding HTTP status codes as specified in the assignment documentation.
    - Configured the application to run on '0.0.0.0' with port '8090'.

- **Replicated_KeyValue_Store.py**
    - Contributed to the design and implementation of vector clock operation to ensure maintaining eventual consistency across the distributed system.
    - Involved in testing the code to identify and rectify errors, ensuring the system's reliability and correctness.
    - Played a role in enhancing the readability and efficiency of the code, making it more maintainable and performant.

Justin Morales
- HTTP_Service.py
    - None

- InMemory_Store.py
    - Coded getting forwarding address, forward requests from client node to main node by creating an API to accept requests and send that information with the proper url to main.

- Replicated_KeyValue_Store.py
    - Designed the key/value store routes and how they function, the broadcasting mechanism we are using, the vector clock functionality, the view routes and their functionality, the mechanism of how the replicas discover each other in a system, the mechanism that checks if a replica is out of date, a mechanism for replicas to discover if another replica has been downed or is not responding so that it may be removed from the system.

Tyler Fong
- HTTP_Service.py
    - None

- InMemory_Store.py
    - Provided assignment 1 to work off from. Merging parts 1 and 2 in git and testing.

- Replicated_KeyValue_Store.py
    - None

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
