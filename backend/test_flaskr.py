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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'who is the new president of USA 2020?',
            'answer': 'Joe Biden',
            'difficulty': 2,
            'category': 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        print('********************************** inside test_get_categories')
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        # print('**********************************')

    def test_get_paginated_questions(self):
        print('********************************** inside test_get_paginated_questions')
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        # print('**********************************')

    def test_404_sent_requesting_beyond_valid_page(self):
        print('********************************** inside test_404_sent_requesting_beyond_valid_page')
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not found')
        # print('**********************************')

    def test_422_if_question_does_not_exist(self):
        print('********************************** inside test_422_if_question_does_not_exist')
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        # print('**********************************')

    def test_delete_questions(self):
        print('********************************** inside test_delete_questions')
        res = self.client().delete('/questions/7')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 7).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 7)
        self.assertTrue(data['questions'])
        self.assertEqual(question, None)
        # print('**********************************')

    def test_create_new_question(self):
        print('********************************** inside test_create_new_question')
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        # print('**********************************')

    def test_search_question(self):
        print('********************************** inside test_search_question')
        res = self.client().post('/questions/search', json={'searchTerm': 'soccer'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        # print('**********************************')

    def test_404_search_question(self):
        print('********************************** inside test_search_question')
        res = self.client().post('/questions/search', json={'searchTerm': 'youbetyoudontgetthisdata'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not found')
        # print('**********************************')

    # {'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '1'}}
    def test_play_quizzes(self):
        print('********************************** inside test_play_quizzes')
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': '1'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        # print('**********************************')

    def test_404_play_quizzes(self):
        print('********************************** inside test_404_play_quizzes')
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'Sciences', 'id': '100'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not found')
        # print('**********************************')

    def test_search_questions_of_categories(self):
        print('********************************** inside test_search_questions_of_categories')
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        # print('**********************************')

    def test_404_search_questions_of_categories(self):
        print('********************************** inside test_404_search_questions_of_categories')
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not found')
        # print('**********************************')

# Make the tests conveniently executable


if __name__ == "__main__":
    unittest.main()
