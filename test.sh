#!/bin/bash


curl http://localhost:5000/echo/get/json \
	 -H "Accept: application/json" 
# {"success":"true"}

curl -X POST http://localhost:5000/echo/post/json \
   	 -H 'Content-Type: application/json' \
   	 -d '{"login":"my_login","password":"my_password"}'
# {"success":"true"}

curl -X PUT http://localhost:5000/echo/put/json \
	 -d "PUT request data"
# {"success":"true"}

curl -X PATCH http://localhost:5000/echo/patch/json \
	 -H 'Content-Type: application/json' \
	 -H 'Accept: application/json' \
	 -d '{"Id": 78912, "Customer": "Jason Sweet", "Quantity": 1}'
# {"success":"true"}

curl -X DELETE http://localhost:5000/sample/delete/json?id=1 \
 	 -H "Accept: application/json"
# {"success":"true"}
