# HTTP_Web_Service
This project originated from CSE138 Distributed System course at University of California Santa Cruz under the assistance of Prof. Liting Hu. 

## HTTP Web Service
- Differentiates between requests with different HTTP verbs (GET/POST) and URI paths (/hello, /hello/<name>, and /test).


## HTTP Interface
### /hello
- Accepts a GET request (with no parameter)
- Return the JSON response body {"message": "world"} and status 200

```python
# Example Python code
def hello_world():
    print("Hello, world!")

```



### Acknowdgegets:

TA: Cheng-Wei Ching

Tutor: Albert Lee

### Team Contributors:

Jun Hayashida

Justin Morales

Tyler Fong

### Citations:
- "Basic Flask operation for Python": https://www.youtube.com/watch?v=Z1RJmh_OqeA
- "key-value store/pair: https://hazelcast.com/glossary/key-value-store/
- "jsonify()": nhttps://www.geeksforgeeks.org/use-jsonify-instead-of-json-dumps-in-flask/#
- "Empty reply from server": moby/moby#2522
- https://www.geeksforgeeks.org/put-method-python-requests/
- https://stackoverflow.com/questions/23144622/how-to-set-http-request-timeout-in-python-flask
- https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
