# Minesweeper API Documentation

The goal of this document is to provide a reference for the RESTful API we have developed for the Minesweeper game. We have thought of the final user as s person using their mobile phone to play the game. Another goal of the document is to detail all important design and implementation decisions that have been taken. 


## Deliverables 
The deliverables of the code challenge are:
1. The URL where the game can be accessed and played (in the  Heroku platform):
>https://minesweeper-api-jr.herokuapp.com/

2. Code in a public Github repo. We have committed gradually with relevant comments, in order to render the development process accessible. 
>https://github.com/gibil5/minesweeper-API


## Support of multiple users and accounts
It is mandatory to login into a session, in order to play the game. The user and password have been sent to evaluators. 


## Languages and frameworks
We have used the following programming languages, frameworks and libraries:
* Django 
* Python (3.9.1 version)
* Javascript 
* HTML5
* CSS3
* Bootstrap library (for styling and responsiveness). 


## REST-API
To implement the REST API, we use the **djangorestframework** library. The API requests are fulfilled using model serializers.
The following models are available through the API:
* User
* Board
* Cell  

Some advantages of using **djangorestframework**:
* It is web browsable.
* Authentication policies including packages for OAuth1a and OAuth2.
* Serialization supports both ORM and non-ORM data sources.
* Highly customizable.

The complete API documentation is in the following link:
>https://minesweeper-api-jr.herokuapp.com/redoc

Another alternative:
>https://minesweeper-api-jr.herokuapp.com/swagger-ui


## Finite State machines 
We are using Finite State Machines, to introduce restrictions into all possible transitions, during the game.  


## Data model 
Three models have been created:
* Board 
* Cell 
* User 


## Database
A Postgres database has been created for data permanence.


## Algorithm 
From the **Ask Python** article:
"Create Minesweeper using Python From the Basic to Advanced"
https://www.askpython.com/python/examples/create-minesweeper-using-python


## Testing 
We have experience with TDD development. So, we always begin by writing a comprehensive 
sets of tests for the most important use cases. We test:
* The Rest API.
* All Views (Board and User).
* Model (Board).


## Deploy in Heroku 
We have chosen Heroku for deployment into production. For several reasons:
* It is a PaaS (Platform as a service), which reduces greatly the amount of time before deployment. 
* It is a polyglot platform (Python, Ruby, Java, Node.js, Scala, Clojure, PHP and Go).
* It has a very flexible pricing structure, that begins with a free (but quite useful) plan. 
* We have previous experience with Heroku, with other frameworks (Ruby on Rails). 
Other possible solutions were Amazon Web Services (EDS+RDS) and Digital Ocean. 

For the moment, we are using a free plan. 
But resources can be improved with a paid plan. 


## Security 


## Dependencies 
We are using the following libraries:
* djangorestframework
* gunicorn
* django-heroku
* requests
* django-cors-headers
* django-fsm
* django-extensions
* django-bootstrap-static
