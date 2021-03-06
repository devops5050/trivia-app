# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies for project

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server for Linux and Mac, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

For Windows cmd, use set instead of export:

set FLASK_APP=flaskr
set FLASK_ENV=development
flask run

You will see output similar to this:

 * Serving Flask app "flaskr" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 802-666-545

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Summary

Trivia API endpoints are REST end points. At high level, it provides following endpoints:

1. GET /categories

    It returns collection of different categories (key/values), success flag.
    
    Sample: curl http://127.0.0.1:5000/categories

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "success": true
        }

2. GET /questions

    It returns collection of categories, questions along with current category, total # of questions and success flag.
    
    Sample: curl http://127.0.0.1:5000/questions

        {
            "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
            }, 
            "current_category": null, 
            "questions": [
                {
                    "answer": "Maya Angelou", 
                    "category": 4, 
                    "difficulty": 2, 
                    "id": 5, 
                    "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                },
                {
                    "answer": "The Palace of Versailles", 
                    "category": 3, 
                    "difficulty": 3, 
                    "id": 14, 
                    "question": "In which royal palace would you find the Hall of Mirrors?"
                }
            ], 
            "success": true, 
            "total_questions": 21
        }

3. DELETE /questions/<int:question_id>
    It deletes specific question from the database based on question id provided in a request object.
    
    Sample: curl -X DELETE http://127.0.0.1:5000/questions/21
    
    On providing wrong question id, following is the output:
    
    {
      "error": 422, 
      "message": "unprocessable", 
      "success": false
    }
    
    Valid quetion id sample: 
    curl -X DELETE http://127.0.0.1:5000/questions/11
    
    {
      "categories": {
        "1": "Science", 
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      }, 
      "current_category": null, 
      "deleted": 11, 
      "questions": [
        {..},
        {..}
       ],
       "success": true,
       "total_questions": 20
   }

4. POST /questions
    It creates a new record in the database based on request object which contains question, its answer, category, and difficulty level.

    Sample curl: 
    
    curl -X POST "http://127.0.0.1:5000/questions"  -d "{\"question\": \"who is the new president of USA?\",\"answer\": \"Brown\", \"difficulty\": 2, \"category\": 3}" -H "Content-Type: application/json"
    
    Output:
    
        {
        "created": 35, 
        "questions": [
            {..},
            {..},
            ], 
            "success": true,
            "total_questions": 24
        }

5. POST /questions/search

    It accepts Search term from user and returns a collection of questions from the database.
    
    Sample URL:
    
    curl -X POST "http://127.0.0.1:5000/questions/search" -d "{\"searchTerm\":\"soccer\"}" -H "Content-Type: application/json"

    Output:

        {
          "questions": [
            {
              "answer": "Brazil", 
              "category": 6, 
              "difficulty": 3, 
              "id": 10, 
              "question": "Which is the only team to play in every soccer World Cup tournament?"
            }
          ], 
          "success": true, 
          "total_questions": 1
        }

6. GET /categories/<category_id>/questions
    It returns a collection of questions against a specific category value from the database.
    
    Sample URL:
    
    curl -X GET "http://127.0.0.1:5000/categories/1/questions"
    
    Output:
    
        {
          "questions": [
            {
              "answer": "The Liver", 
              "category": 1, 
              "difficulty": 4, 
              "id": 20, 
              "question": "What is the heaviest organ in the human body?"
            }, 
            {
              "answer": "Blood", 
              "category": 1, 
              "difficulty": 4, 
              "id": 22, 
              "question": "Hematology is a branch of medicine involving the study of what?"
            }
          ], 
          "success": true, 
          "total_questions": 2
        }

7. POST /quizzes
    It returns a set of questions based on category selected or questions for all categories.
    
    It also keeps track of previously asked questions so that previously asked questions are not repeated.
    
    Sample Curl URL:
    
    curl -X POST "http://127.0.0.1:5000/quizzes" -d "{\"quiz_category\":{\"type\": \"Science\", \"id\": \"1\"},\"previous_questions\":[]}" -H "Content-Type: application/json"


        {
          "question": {
            "answer": "Blood", 
            "category": 1, 
            "difficulty": 4, 
            "id": 22, 
            "question": "Hematology is a branch of medicine involving the study of what?"
          }, 
          "success": true
        }


## Error Handling
Errors are returned as JSON objects in the following format:

{
  "error": 404, 
  "message": "Resource Not found", 
  "success": false
}

The API will return following errors when request fails:

1. 400: Bad Request
2. 404: Resource Not Found
3. 422: Not processable


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## Troubleshooting Tips

During initial setup / run, if following error is observed:

TypeError: required field "type_ignores" missing from Module

Please perform below steps:

pip3 install --upgrade werkzeug 
(Link: https://stackoverflow.com/questions/60140174/basic-flask-app-not-running-typeerror-required-field-type-ignores-missing-fr)
