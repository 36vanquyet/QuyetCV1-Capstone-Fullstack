# Capstone Full Stack
## Casting Agency Project
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Roles:
- Casting Assistant
    + Can view actors and movies
- Casting Director
    + All permissions a Casting Assistant has and…
    + Add or delete an actor from the database Modify actors or movies
- Executive Producer
    + All permissions a Casting Director has and…
    + Add or delete a movie from the database


## 1. Run on the local machine
### Step 1: Setup the local database for running.
```
dropdb casting
createdb casting
```
![database_run](./images/database_run.png)

### Step 2: Auth0 Setup
#### Create application Auth0
![application_auth0](./images/application_auth0.png)
#### Create API Auth0 and Permission
![api_permission](./images/api_permission.png)
#### Create Auth0 Roles
![roles](./images/roles.png)
#### Create User Permission 
##### Casting Assistan Permission:
- `get:actors`
- `get:movies`

![casting_assistan](./images/user_casting_assistan.png)

##### Casting Director Permission:
- `get:actors`
- `get:movies`
- `post:actors`
- `patch:actors`
- `delete:actors`
- `patch:movies`

![casting_director](./images/user_casting_director.png)

##### Executive Producer Permission:
- `Full access`

![executive_producer](./images/user_executive_producer.png)

### Step 3: Run Local Backend Server
#### Install all requirement
```
pip install -r requirements.txt
```
#### Set environment variable
##### - If you use the Command Prompt on Windows
```
set DB_NAME=<your database name>
set DB_USER=<your username>
set DB_PASSWORD=<your password>
set DB_HOST=<your host>
```
##### - If you use the terminal on Unix
```
export DB_NAME=<your database name>
export DB_USER=<your username>
export DB_PASSWORD=<your password>
export DB_HOST=<your host>
```
#### Run backend server
```
python api.py
```
![local_backend_server](./images/run_local_backend_server.png)

## 2. Test Endpoint
### Step 1: Setup the local database for testing
```
dropdb casting_test
createdb casting_test
```
### Step 2: Run test api
```
python test_api.py
```
Results:
![test_api](./images/test_api.png)

## 3. Test Postman Collection
### Step 1: Import Postman Collection
1. Open Postman
2. Click on Import
3. Click on Choose Files
4. Select the file `quyetcv1-capstone-fullstack.postman_collection.json`

### Step 2: Get JWT Tokens
Access the following link to get the JWT tokens for the users:
```
https://quyetcv1.us.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=p48LL0YixcKDFKGOyPXGoY8FO0rjUj3V&redirect_uri=http://localhost:8100/results
```
Then, import Bearer Tokens into Postman.

Token `Casting Assistant` when create README.md:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTVhNTI0NjVhYWZlOGU4NzQyODc3NGUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDA0MTg2OTMsImV4cCI6MTcwMDUwNTA5MywiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.XXNgOO8wWrlgepw1rdKzaeh5lAJFIHFV-Jg7LDZMUDDhPjqaYJLWTNm29k5PUDcZrn_OMli0DAyTQUi6JggQ23STX0ROH39fVfUR4kmGbIzAbZSANpeMyaMw5VQgk04U86zu3GRO_RTtW7gAY0jvo1AsWh9VfdIQ6xmotSs3vkZ6nbcu0JRwpN7Kg-tUGsjM4qIsE1q-9Wnybqw66G6ZbXX_45KyDpdHpPzCIXejR7tw9k4mGYHWa6S4VIsCEGueMNblvoFWY8AzQaQXn-DS_opJ-F-FT-GUob94Bh9ZKSyBqNdwDDT8jiEOZiqDSVYsIvGFC-rCiFFaNZcNbl6H5w
```

Token `Casting Director` when create README.md:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTVhNTU0YTg3Y2IzMDAzYzg2ZWFiZDgiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDA0MTg5OTYsImV4cCI6MTcwMDUwNTM5NiwiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.H05d4isF33-aR1sn-S-C0CSN_XCHmFR_Z-sW4KX2pmdeoPN_QkA2RLLUX970l5dadVKGtGh4WBKSfEIeF9vamnSvy7ez4uWSzQWPpogALTgrUkBCEmytGOGtZW2BU0n-OP_NwLJhI31I_VLTBILI0glkYuPaNIMttjJZb8GC_OlVS6F0t_OpnmwESunJbhUOMknLlwYhIXALwqVfuDN3obciETmP6imIw0K2PfpqQpLo-pjnmPRYM5r0XPkXtJVtTBNDCikvguMV7FVxQMwD0vyxKwjxKCM5X1HYqDnE78UihIP2sXib6L_5BhRNt0LNlENxuf-Tyf_ey_8ja3b1lA
```

Token `Excutive Producer` when create README.md:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTVhNTYyNTg3Y2IzMDAzYzg2ZWFjNTUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDA0MTkxODIsImV4cCI6MTcwMDUwNTU4MiwiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BpP34UzzeWVb8xPyk6u2JfMK-gO_1oaCD8Ijrk7m1ucXBZW6MODj_gyDPhUt9mI08bnyYpnKgeiyJWUo-N7MQ835KMa-cYJH2nUOILR4DQCP83ggnTXqtRSXYWb6W0kc3Tt8HuuaIMCE5QcDH0KtYH7zvo5zgBt6h_Bp-TkxAerNZDqgodM1WKbYkkhqOFrtGgJVYnrInRCnA2t_DFnMHIso__VTZoyG0276Zkg6OOd7AyEsb4FZkG46kWOKKJW2FldBMvnKqScKnDKfz2baBUqsFJcnA513rhroKIb-yBYajE0DPahvynSHlwyxdPx6EYQRlTF6KqI0DsqMc4keKg
```

If the token is expired, please access the <a href="https://quyetcv1.us.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=p48LL0YixcKDFKGOyPXGoY8FO0rjUj3V&redirect_uri=http://localhost:8100/results">link</a> above to get the new token.

Account Casting Assistant:
```
Email: casting_assistant@gmail.com
Password: casting_assistant123
```
Account Casting Director:
```
Email: casting_director@gmail.com
Password: casting_director123
```
Account Excutive Producer:
```
Email: excutive_producer@gmail.com
Password: excutive_producer123
```

Return URL with bearer token:
```
http://localhost:8100/results#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRvTEd4dzVEUHplVVNTb0h1Wmt3TSJ9.eyJpc3MiOiJodHRwczovL3F1eWV0Y3YxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTVhNTYyNTg3Y2IzMDAzYzg2ZWFjNTUiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjUwMDAiLCJpYXQiOjE3MDA0MTkxODIsImV4cCI6MTcwMDUwNTU4MiwiYXpwIjoicDQ4TEwwWWl4Y0tERktHT3lQWEdvWThGTzByalVqM1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.BpP34UzzeWVb8xPyk6u2JfMK-gO_1oaCD8Ijrk7m1ucXBZW6MODj_gyDPhUt9mI08bnyYpnKgeiyJWUo-N7MQ835KMa-cYJH2nUOILR4DQCP83ggnTXqtRSXYWb6W0kc3Tt8HuuaIMCE5QcDH0KtYH7zvo5zgBt6h_Bp-TkxAerNZDqgodM1WKbYkkhqOFrtGgJVYnrInRCnA2t_DFnMHIso__VTZoyG0276Zkg6OOd7AyEsb4FZkG46kWOKKJW2FldBMvnKqScKnDKfz2baBUqsFJcnA513rhroKIb-yBYajE0DPahvynSHlwyxdPx6EYQRlTF6KqI0DsqMc4keKg&expires_in=86400&token_type=Bearer
```

### Step 3: Test Endpoints
1. Click on the arrow next to the collection name to expand the collection.
2. Choose folder `Casting Assistant`, `Casting Director`, or `Executive Producer` and run tests on the endpoints

Results:
- All test should pass for `Casting Assistant` folder.
![test_assistant_1](./images/pm_cas_assistant_1.png)
![test_assistant_2](./images/pm_cas_assistant_2.png)
![test_assistant_2](./images/pm_cas_assistant_3.png)
- All test should pass for `Casting Director` folder.
![test_director_1](./images/pm_cas_director_1.png)
![test_director_2](./images/pm_cas_director_2.png)
![test_director_2](./images/pm_cas_director_3.png)
- All test should pass for `Executive Producer` folder.
![test_ex_producer_1](./images/ex_producer_1.png)
![test_ex_producer_2](./images/ex_producer_2.png)
![test_ex_producer_3](./images/ex_producer_3.png)

Export the collection overwriting the `quyetcv1-capstone-fullstack.postman_collection.json` file.

## 4. Deployment
![deloyment](./images/deloyment.png)
### Step 1: Register account on Render
### Step 2: Create PostgreSQL
![postgresql_render](./images/postgresql_render.png)

Internal Database URL:
```
postgres://quyetcv1:geOGfT0WevH0cMo5itp2TUyYsLNtm3Ko@dpg-cld5nueg1b2c73f4b9u0-a/casting_8y55
```

External Database URL:
```
postgres://quyetcv1:geOGfT0WevH0cMo5itp2TUyYsLNtm3Ko@dpg-cld5nueg1b2c73f4b9u0-a.oregon-postgres.render.com/casting_8y55
```

### Step 3: Create Web Service to run server
![web_service](./images/web_server.png)

Endpoint Render URL: https://capston-fullstack.onrender.com

### Step 4: Test Server live

#### Test with token Casting Assistant:
![get_actors_with_assistant](./images/get_assistant.png)

#### Test with token Casting Director:
![get_movies_with_director](./images/get_director.png)

#### Test with token Executive Producer:
![delete_movies_with_ex_producer](./images/delete_ex_prodecer.png)

#### Log Server
![log_server](./images/Log_server.png)

## Documentation
### 1. API Reference
URL host: http://localhost:5000/

#### Endpoints
`GET /actors`
- Fetches a list of `actors` in the database
- Permission required: `get:actors`
- Request Arguments: `None`
- Returns: An object with a single key, actors, that contains an array of actors objects.
```
{
    "actors": [
        {
            "age": 34,
            "gender": "Male",
            "id": 1,
            "name": "Daniel Radcliffe"
        },
        {
            "age": 23,
            "gender": "Female",
            "id": 2,
            "name": "Hamabe Minami"
        }
    ],
    "success": true
}
```

`GET /movies`
- Fetches a list of `movies` in the database
- Permission required: `get:movies`
- Request Arguments: `None`
- Returns: An object with a single key, movies, that contains an array of movies objects.
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Tue, 01 Jan 2002 00:00:00 GMT",
            "title": "Harry Potter"
        },
        {
            "id": 2,
            "release_date": "Thu, 01 Jan 2009 00:00:00 GMT",
            "title": "Godzilla Minus One"
        }
    ],
    "success": true
}
```
`POST /actors`
- Creates a new `actor` in the database
- Permission required: `post:actors`
- Request Arguments: json
```
{
    "name": <actor name>,
    "age": <actor age>,
    "gender": <actor gender>
}
```
- Returns: An object with a single key, actors, that contains an array of actors objects.
```
{
    "actors": [
        {
            "age": 24,
            "gender": "male",
            "id": 3,
            "name": "QuyetCV1"
        }
    ],
    "success": true
}
```

`POST /movies`
- Creates a new `movie` in the database
- Permission required: `post:movies`
- Request Arguments: json
```
{
    "title": <movie title>,
    "release_date": <release date movie>
}
```
- Returns: An object with a single key, movies, that contains an array of movies objects.
```
{
    "movies": [
        {
            "id": 3,
            "release_date": "Thu, 01 Jan 2009 00:00:00 GMT",
            "title": "Godzilla Minus One"
        }
    ],
    "success": true
}
```

`PATCH /actors/<id>`
- Updates a new `actor` in the database
- Permission required: `patch:actors`
- Request Arguments: json
```
{
    "name": <actor name>,
    "age": <actor age>,
    "gender": <actor gender>
}
```
- Returns: An object with a single key, actors, that contains an array of actors objects.
```
{
    "actors": [
        {
            "age": 24,
            "gender": "male",
            "id": 3,
            "name": "QuyetCV1"
        }
    ],
    "success": true
}
```

`PATCH /movies/<id>`
- Updates a new `movie` in the database
- Permission required: `patch:movies`
- Request Arguments: json
```
{
    "title": <movie title>,
    "release_date": <release date movie>
}
```
- Returns: An object with a single key, movies, that contains an array of movies objects.
```
{
    "movies": [
        {
            "id": 3,
            "release_date": "Thu, 01 Jan 2009 00:00:00 GMT",
            "title": "Godzilla Minus One"
        }
    ],
    "success": true
}
```
`DELETE /actors/<id>`
- Deletes a `actor` in the database
- Permission required: `delete:actors`
- Request Arguments: `None`
- Returns: An object with a single key, actors, that is a message notification.
```
{
    "message": "Actor id=1 deleted successfully",
    "success": true
}
```

`DELETE /movies/<id>`
- Deletes a `movies` in the database
- Permission required: `delete:movies`
- Request Arguments: `None`
- Returns: An object with a single key, movies, that is a message notification.
```
{
    "message": "Movie id=1 deleted successfully",
    "success": true
}
```

### 2. Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 404,
    "message": "Movie with id 255 not found",
    "success": false
}
```
The API will return three error types when requests failed:
+ `400`: Bad Request
+ `401`: Unauthorized
+ `403`: Forbidden
+ `404`: Resource Not Found
+ `422`: Not Processable

### 3. Users and Roles

#### Casting Assistant
+ Can view actors and movies

#### Casting Director
+ All permissions a Casting Assistant has and…
+ Add or delete an actor from the database Modify actors or movies

#### Executive Producer
+ All permissions a Casting Director has and…
+ Add or delete a movie from the database