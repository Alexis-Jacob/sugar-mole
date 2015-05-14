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

	
### 2 House:
* url:  ```http://54.72.214.104/api/house/```
* method: ```GET```
    * Get all the informations about all the house
    * You can add the uuid of the house at the end in order to get the information avbout a given house: ```http://54.72.214.104/api/house/b26d86c6-4864-4a29-ad07-3516f2bd5305/```
    * Return a json list of the scenarios (conditions and actions)

* method: ```POST```
    * Create a new house
    * return: ```HTTP_201``` with the description of the house in the ```response```field
    > *hint: save the uuid of the house*

* method: ```PUT```
















dsfsdf