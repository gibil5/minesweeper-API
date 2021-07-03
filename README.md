# Minesweeper API Documentation

J. Revilla , 3 July 2021

The goal of this document is to provide Specifications for the Minesweeper Game RESTful API. We have thought of the final user as a person using their mobile phone to play the game. 
Another goal of the document is to detail important design and implementation decisions. 

## Deliverables 
The deliverables of the code challenge are:

1. The URL where the game can be accessed and played (in the  Heroku platform):
>https://minesweeper-api-jr.herokuapp.com

2. Code in a public Github repo. We have committed gradually with relevant comments, in order to render the development process accessible:
>https://github.com/gibil5/minesweeper-API

## Support of multiple users
It is mandatory to login into a session, in order to play the game. 
The user and password have been sent to evaluators. 

## Languages and frameworks
We have used the following programming languages, frameworks and libraries:
* Django (3.1.4)
* Python (3.9.1)
* Javascript 
* HTML5
* CSS3
* Bootstrap library (for styling and responsiveness)

## REST API
To implement the REST API, we use the **djangorestframework** library. The API requests are fulfilled using model serializers.
The following models are available through the API:
* User
* Board
* Cell  

The complete API documentation is in the following link:

>https://minesweeper-api-jr.herokuapp.com/redoc

Some advantages of using **djangorestframework**:
* It is web browsable.
* Authentication policies including packages for OAuth1a and OAuth2.
* Serialization supports both ORM and non-ORM data sources.
* Finally, it is highly customizable.

## Finite State machines 
We are using Finite State Machines, to introduce restrictions into all possible transitions during the game. This facilitates testing greatly. For implementation, we use the **django-fsm** library:

## Database
A Postgres database has been created for data permanence.
To store and manage the following data:
* Board 
* Cell 
* User 

## Algorithm 
For the Minesweeper game algorithm, we have used the following article: 

"Create Minesweeper using Python From the Basic to Advanced".
From the AskPython website.
> https://www.askpython.com/python/examples/create-minesweeper-using-python

## Testing 
We have written a comprehensive sets of tests, using the **unittest** package. We have written  the following test cases:
* The Rest API.
* All Views (Board and User).
* Models (Board, Cell and User).

## Deployment 
We have chosen Heroku for deployment into production. It is a great platform for several reasons:
* It is a PaaS (Platform as a service), which reduces the  deployment cycle. 
* It is polyglot: Python, Ruby, Java, Node.js, Scala, Clojure, PHP and Go.
* It has a flexible pricing structure that begins with a free plan. 
* Finally, we have previous experience using Heroku.

Other possible solutions were: AWS and Digital Ocean. 

## Security 
The following measures have been taken to improve security:
* Heroku provides by default an encrypted connection (https).
* The sensitive settings variables (SECRET_KEY and DEBUG) are read from environment variables on Heroku. 
* Access to the game requires login. 
* Finally, all Django forms can be protected against CSRF (Cross site request forgery).
