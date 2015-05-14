# Api Sugar Mole

### 1 User:
* url: ```http://54.72.214.104/api/user/```
* method: ```GET```
	* Get the list of users (for debug only
* method: ```POST```
	* Register a new user 	
	* body param: ```username``` and ```password``` 
	```javascript
  {
      "username" : "toto",
      "password" : "pass",
  }
  ```
  * return:  
     + ```HTTP_201``` with a token in the field ```token``` if everything went well
     + ```HTTP_400``` with an explicit response in the field ```response``` if something went wrong *(user already in use...)*
    

* method: ```PUT```
	* Connect an user (in order to get the *token*)
	* body param: ```username``` and ```password``` 
	```javascript
  {
      "username" : "toto",
      "password" : "pass",
  }
  ```
  * return:
  	* ```HTTP_200``` with a token in the field ```token```` if everyting went well
  	* ```HTTP_400```  with an explicit response in the field ```response``` if something went wrong *(user already in use...)*
  	* ```HTTP_401``` if the password is wrong

	