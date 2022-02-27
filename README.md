# BMG_tech_test_API
This app is developed as requirement for Boston Makmur Gemilang recruitment process.
This app acts as endpoints for API requests.
System specification is also included in this repository so that this app can be built on docker.
To built the app, follow the instruction below:
1. Git clone this repository
2. Navigate into the downloaded direcotry
3. Run code below:
```
docker-compose build
```
```
docker-compose up
```
4. The app is up inside containers.


There are six enpoints provided by this app:
1. '/registration'
This endpoint validates and registers new user to the system. This endpoint uses post method and requires these following fields
- username  : alphanumeric
- password  : alphanumeric
- name      : alphanumeric
- email     : valid email

2. '/login'
This endpoint validates user. A validated user will be assigned with a token that activate for 30 minutes. The required fields are:
- username  : alphanumeric
- password  : alphanumeric

3. '/edit_data'
This endpoint enables user to change their data. Previously assigned token is validated in this endpoint. The required fields are:
- Token     : generated at login process
- parameter to be changed : name of data that user want to change (Only a parameter can be changed at a time)
- new value : new data that will be added to the database
- referral 
