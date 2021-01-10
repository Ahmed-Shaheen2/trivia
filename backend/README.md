# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

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

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

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

## ApI Documentation
```
hint: all endpoints returns a key 'success' with a value True if successfully executed

available Endpoints list
GET '/categories'                               // list all categories
GET '/questions'                                // get all questions paginated to 10 questions for page
DELETE '/questions/<int:question_id>'           // delete a question by it's id
POST 'questions'                                // add a new question
POST '/search-questions'                        // search questions by a phrase 
GET '/categories/<int:category_id>/questions'   // get questions in a specific category paginated to 10 per page
POST '/quizzes'                                 // get randomly choosen question from all questions or from the specified category depeneding on the request payload (more details below)

-----------------

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a key 'total_categories' whose value is number of categories available and the key 'categories' that contains a object of id: category_string key:value pairs.
- example
{
    'categories': {'1' : "Science",
                    '2' : "Art",
                    '3' : "Geography",
                    '4' : "History",
                    '5' : "Entertainment",
                    '6' : "Sports"
                    },
    'total_categories': 6
}

-----------------

GET '/questions' 
- use this to get paginated lists of all questions regardles what category they belongs to
- Request Arguments: query parameter wth the key page and value is the number of the wanted page knowing that every page contains 10 questions
- Returns: four keys questions: which is list of 10 questions selected from all questions depeneding on the specified page, total_questions: number of all questions whatever category they belongs to, categories: dictionsary of categories like the categories in the previous endpoint , current_category: None i this case because there is no specified category in this endpoint
- example
{
    'success': true,
    'questions': [
        {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },...,... // ten questions in the list at maximum 
    ],
    'total_questions': 19,
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    'current_category': None
}

-----------------

DELETE '/questions/<int:question_id>'
- use this to delete a question by it's id
- Request Arguments: there is no arguments except the id which is sent as a part of the path like specified above not as an argument
- Returns: nothing except the success key hinted at the beginning in case of successfully deleted the question

-----------------

POST 'questions'

- use this to submit a new question to be stored in the database
- Request Arguments: this endpoints requires a json payload of four mandatory keys (question, answer, difficulty, category) and will return an error in case of one of them is mising. question: a string of the question to be stored, answer: a string of the correct answer of the question, difficulty: an integer from 1 to 5 illustrating how difficult of this question, category: an integer of the id of the category that the question belongs to
- Returns: nothing except the success key hinted before in case of succesfully question stored in the database

POST '/search-questions'
- use this to search for questions using a search parameter that specified in payload
- Request Arguments: a json payload that contains only one key 'searchTerm' whose value is the term to search questions for
- Returns: returns a response which exactly similar to the GET '/questions' endpoint response but here questions are filtered by the search term specified and the total_questions are only the number of questions containing the search term
- example
{
    'success': true,
    'questions': [
        {
            "answer": "Maya Angelou", 
            "category": 4, 
            "difficulty": 2, 
            "id": 5, 
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },...,... // ten questions in the list at maximum 
    ],
    'total_questions': 11,
    'categories': {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    'current_category': None
}

-----------------

GET '/categories/<int:category_id>/questions'
- use this to get list of questions in one category only paginated to 10 questions per page
- Request Arguments: no arguments except the id of the category to get it's questions but it's being sent as a part of the uri as illustrated above 
- Returns: returns a response which exactly similar to the GET '/questions' endpoint response but here questions are filtered by the category whose id specified in the uri and the total_questions are only the number of questions in this category only
- example
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": {
    "id": 1, 
    "type": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}

-----------------

POST '/quizzes'  
- this enpoint returns a randoly choosen question from all questions or from a specified category whose id is not included in the previous_questions list specified in payload
- Request Arguments: json object with two keys previous_questions which is a list of questions ids that picked before and quiz_category which is an object specifing the category to choose from or all to choose from all questions
- request payload example
{
    previous_questions: [3, 8, 11],
    quiz_category: {
        type: "all",
        id: "0"
    }
}
- Returns: a json object with question key that contains the question in it's value like below
- example
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```