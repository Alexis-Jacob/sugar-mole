# Api Sugar Mole

### 1 User:
* Url: ```http://54.72.214.104/api/user/```
* Method: ```GET```
	* Get the list of users (for debug only
* Method: ```POST```
	* Register a new user 	
	* Body param: ```username``` and ```password``` 
	```javascript
  {
      "username" : "toto",
      "password" : "pass",
  }
  ```
  * Return:  
     + ```HTTP_201``` with a token in the field ```token``` if everything went well
     + ```HTTP_400``` with an explicit response in the field ```response``` if something went wrong *(user already in use...)*
    

* Method: ```PUT```
	* Connect an user (in order to get the *token*)
	* Body param: ```username``` and ```password``` 
	```javascript
  {
      "username" : "toto",
      "password" : "pass",
  }
  ```
  * Return:
  	* ```HTTP_200``` with a token in the field ```token```` if everyting went well
  	* ```HTTP_400```  with an explicit response in the field ```response``` if something went wrong *(user already in use...)*
  	* ```HTTP_401``` if the password is wrong

	
### 2 House:
* Url:  ```http://54.72.214.104/api/house/```
* Method: ```GET```
    * Get all the informations about all the house
    * You can add the uuid of the house at the end in order to get the information avbout a given house: ```http://54.72.214.104/api/house/b26d86c6-4864-4a29-ad07-3516f2bd5305/```
    * Return a json list of the scenarios (conditions and actions)

* Method: ```POST```
    * Create a new house
    * return: ```HTTP_201``` with the description of the house in the ```response```field
    > *hint: save the uuid of the house*

* Method: ```PUT```
	* Add or remove a scenario from the house
	* Url: ```http://54.72.214.104/api/house/b26d86c6-4864-4a29-ad07-3516f2bd5305/```
	* Body param:  
		- ```scenario_name``` with the name of the scenario
		- ```option``` to add or remove; value are ```add``` or ```everything not add``` 
		- exemple:
		```javascript
		{
			"scenario_name" : "alarm_001",
			"option" : "add"
		}
		```
    - ```api``` if you want to register to a new api: the other parameters depends on the api (check #3)

	* Return: ```HTTP_200````or ```HTTP_404```



### 3 Api Details:
* Url:  ```http://54.72.214.104/api/apiDetails/```
* Method: ```GET```
    * Get all the informations needed in order to register a new trademark 
    * Return a json list of api name and parameters 