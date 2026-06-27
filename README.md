# fast-api-app-

## creating fastapi application

## CRUD operation
-create
-Read
-update
-Delete

## rest API
-get
-post

## status codes
-400 bad request
-401 unauthorized
-403 Forbidden
-404 Not found
-405 method not allowed
-409 conflict
-500 internal server error

## Architecture of fastapi application
-Model- tables creation
-router--routes requests to controllers
-controller--controller logic
-service--business logic
-Repository--data access layer
-Middleware--requesting processing pipeline

# database
## relatinal database
--mysql
--postdresql
-sql
-sqlite
## non-relational database
-dynamodb
-redis
-mongodb

# constraints in database
-primary key--eg:student_id
-foreign key--eg:department_id in student table
-unique --eg:email,phonenumber
-not null --eg:name
-check --eg:salary>0
default eg:-timestamp:func.now()


# modules
-sqlalchemy--orm(object relational mapping)
-fastapi--web framework
-uvicorn--server for running fastapi 
application--> `uvicorn app.main:app --relaod`
psycopg2--postgresql driver
pydantic --data validation
-typing-extension--type hints

# concepts
-ORM
object relational mapping-->to convert to the python code to the sql code without writing the sql commands

-Depends
Dependency Injection--->to inject dependencies to route handlers

-Sessionmaker
To create a session with database

-SessionLocal
To craete a session with the database for a single request

-declarative_base
To createbase class for all the models

