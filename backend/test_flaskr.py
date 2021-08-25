import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://postgres:root@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        # test variables
        self.new_question = {
            'question': 'After what war was Berlin divided into two cities?',
            'answer': 'WWII',
            'difficulty': 1,
            'category': 4
        }

        self.search = {
            'searchTerm' : 'artist'
        }

        self.bad_search = { 
            'searchTerm' : 'absjghewifn'
        }

        self.next_question = {
            'previous_questions': [],
            'quiz_category': 'Art'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_success_categories(self):
        print(""" Test GET /categories success """)
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
    
    def test_405_method_not_allowed(self):
        print("""Test POST /categories (405) failure """)
        res = self.client().post('/categories', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_paginated_questions(self):
        print(""" Test GET /questions success """)
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['currentCategory'], '')
        self.assertTrue(len(data['questions']))

    def test_404_requesting_beyond_valid_page(self):
        print(""" Test GET /categories failure (404) """)
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_questions_for_category(self):
        print(""" Test GET /categories/id/questions success """)
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
        self.assertEqual(len(data['questions']), 3)
    
    def test_get_questions_for_nonexistent_category(self):
        print(""" Test GET /categories/id/questions failure (404) """)
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_success(self):
        print("""Test DELETE /questions/id success """)
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_failure_422(self):
        print("""Test DELETE /questions/id failure """)
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_quizzes_next_question(self):
        print("""Test POST /quizzes success """)
        res = self.client().post('/quizzes', json=self.next_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    def test_422_no_data_quizzes_question(self):
        print("""Test POST /quizzes failure (no data) """)
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request') 
    
    def test_post_success_questions_add(self):
        print("""Test POST /questions add success """)
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_post_questions_add_no_data(self):
        print("""Test POST /questions failure (no data) """)
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_questions_search_with_results(self):
        print("""Test POST /questions search success """)
        res = self.client().post('/questions', json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['currentCategory'])
        self.assertEqual(len(data['questions']), 2)
        self.assertTrue(data['totalQuestions'])   
    
    def test_questions_search_without_results(self):
        print("""Test POST /questions search success """)
        res = self.client().post('/questions', json=self.bad_search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['currentCategory'])
        self.assertEqual(len(data['questions']), 0)
        self.assertTrue(data['totalQuestions'])  
  

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()