# Trivia API Project

This project is a trivia game simulator for the Udacity Fullstack WebDevelopment nanodegree. You can add questions and play a trivia game where you will choose a category and gain points for how many questions you answer correctly.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns a dictionary of categories where the keys are the category ID and the value is the category string
    - Request Args: None
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
  "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
"success": true
}
```

#### GET /questions
- General:
    - Fetches a paginated set of questions (10), a total number of questions, all categories and the current category (if set)
    - Request Args: Optional page (integer)
- `curl http://127.0.0.1:5000/questions?page=2`
```
{
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
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
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "WWII",
      "category": 4,
      "difficulty": 1,
      "id": 24,
      "question": "What war was the second world war?"
    }
  ],
  "totalQuestions": 20,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "",
  "success": true
}
```
#### GET /categories/{category_id}/questions
- General:
    - Returns questions for a category specified by the id request argument
    - Request Args: category_id - integer
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

``` 
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
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "totalQuestions": 20,
  "currentCategory": "Science",
  "success": true
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns appropriate HTTP status code and the ID of the question deleted.
    - Request Args: question id - integer
- `curl -X DELETE http://127.0.0.1:5000/questions/21`
```
{
  "success": true,
  "id": 21
}
```
#### POST /quizzes
- General:
    - Sends a post request in order to get the next quiz question.
    - Request Args: None 
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20], "quiz_category": {"type": "Science", "id": "1"}}'`
```
{
  "question":
    {
      "id": "Hematology is a branch of medicine involving the study of what?",
      "question": 22,
      "answer": "Blood",
      "difficulty": 4,
      "category": "1"
    },
  "success": true,
}
```

#### POST /questions
- General:
    - Sends a post request in order to add a new question.
    - Request Args: None 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "This is a new question", "answer": "This is a new answer", "difficulty": 1, "category", 1}'`
```
{
  "success": true,
}
```

#### POST /questions
- General:
    - Sends a post request in order to search for a list of questions matching a term.
    - Request Args: None 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "aut"}'`
```
{
   "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "totalQuestions": 2,
  "currentCategory": "",
  "success": true
}
```



