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
    - ```add_member``` if you want to register an user to the house

	* Return: ```HTTP_200````or ```HTTP_404```



### 3 Api Details:
* Url:  ```http://54.72.214.104/api/apiDetails/```
* Method: ```GET```
    * Get all the informations needed in order to register a new trademark 
    * Return a json list of api name and parameters 

### 4 Devices infos:
* Url: ```http://54.72.214.104/api/devicesInfo/```
* Method: ```GET```
  * Return all the devices available, with type, desc and extra informations (in order to réuse it)
  * type:
    + 1: Weather station, desc can contain temperature/humidity and optionnaly CO2
    + 2: Wind infos, desc can contain   WindStrength, GustStrength, GustAngle, WindAngle

  *ex: 
  ```json
  [
    {
        "type": 1, 
        "data": "{\"api\": \"netatmo\", \"device_id\": \"02:00:00:00:02:a0\"}", 
        "name": "Netatmo HQ", 
        "desc": {
            "temperature": 19.8, 
            "humidity": 54
        }
    }, 
    {
        "type": 2, 
        "data": "{\"api\": \"netatmo\", \"device_id\": \"06:00:00:00:00:cc\"}", 
        "name": "Anémomètre", 
        "desc": {
            "WindStrength": 6, 
            "GustStrength": 10, 
            "GustAngle": 104, 
            "WindAngle": 135
        }
    }, 
    {
        "type": 1, 
        "data": "{\"api\": \"netatmo\", \"device_id\": \"03:00:00:00:1c:24\"}", 
        "name": "Coffee Machine", 
        "desc": {
            "CO2": 770, 
            "temperature": 24.4, 
            "humidity": 43
        }
    }, 
    {
        "type": 1, 
        "data": "{\"api\": \"netatmo\", \"device_id\": \"03:00:00:00:9f:1e\"}", 
        "name": "Meeting Room", 
        "desc": {
            "CO2": 983, 
            "temperature": 23, 
            "humidity": 48
        }
    }, 
    {
        "type": 1, 
        "data": "{\"api\": \"netatmo\", \"device_id\": \"02:00:00:04:c5:b4\"}", 
        "name": "Outdoor", 
        "desc": {
            "temperature": 23.2, 
            "humidity": 47
        }
    }
  ]
  ```
  * Method : "Put"
  * body param : "data" --> data field returned when devicelist with get
  * rep ```javascript
    {
      "type": 1, 
      "data": "{\"api\": \"netatmo\", \"device_id\": \"02:00:00:00:02:a0\"}", 
      "name": "Netatmo HQ", 
      "desc": {
          "temperature": 19.7, 
          "humidity": 54
      }
  }
  ```