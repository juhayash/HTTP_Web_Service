# HTTP_Web_Service
This project originated from CSE138 Distributed System course at University of California Santa Cruz under the assistance of Prof. Liting Hu. 

## HTTP Web Service
- Differentiates between requests with different HTTP verbs (GET/POST) and URI paths (/hello, /hello/<name>, and /test).


## HTTP Interface
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
