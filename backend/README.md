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

# Alembic
pip install alembic

alembic init alembic

alembic -> env.py -> from imported model -> metadata data

alembic.ini -> sqlalchemy.url to postgresql database url

postgresql://user:password@host:port/database_name

alembic revision --autogenerate -m "initial migration"

alembic upgrade head


npm install vite@latest
npm create vite@latest talentspark
cd talentspark/
npm run dev


# npm
1  npm install vite@latest
2  npm create vite@latest talentspark
3  cd talentspark/
4  npm run dev
5  javascript -> ES6 -> arrow functions, rest and spread,
   template literals, destructuring, promises, async/await
6  dom-> document object manipulation
7  vitual dom-> react virtual dom->copy of original dom
   which will update react dom and then updated dom will
   be updated in real dom
8  components-which are different sections of the web page


npm install axios
uvi->axios->localhost:8000(api call)
(python)->db->useeffect->setstate->render->ui


useEffect - which is used to call the api or which is used to fetch the data from the api automatically when the page is loaded

useState - which is used to store the data in the component and which will update the component when the data is updated or changed        

promise--handles asyn operations

asyncronise- handles multiple request



## hashing algorithm
argon2
bcrypt
python-jose[cryptography]- used to create jwt tokens
jwt tokens -> used to authenticate and authorize users
its in format xxxx.yyyyy.zzzz basically 3 parts
1.header -> algo + token type:{alg:HS256,typ:JWT}
2.payload -> data, for eg: {user_id:1,role:admin}
3.signature -> used to verify the token:{hash(header+payload+secretkey)}
access token -> used to access protected resourcesrefresh token -> used to refresh access tokenpip install python-multipart

pip install python multipart


