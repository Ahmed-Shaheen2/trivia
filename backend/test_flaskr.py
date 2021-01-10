import os
import random
from typing import Dict
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
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def json(self, route):
        return json.loads(self.client().get(route).data)

    """
    I'm going to number my test functions after the prefix "test_"
    to force unittest to execute them in the expected order from top to bottom
    because unittest basicaly orders all test functions alphabeticaly
     not according to their defining order
    """

    def test_01_get_all_categories(self):
        response = self.json('/categories')

        # define a global db_categories and db_questions_count to use it every where when i need it ... why?
        # to reduce database queries as much as possible
        global db_categories
        db_categories = Category.query.all()

        global db_questions_count
        db_questions_count = Question.query.count()

        self.assertEqual(response['success'], True)
        self.assertDictEqual({str(cat.id): cat.type
                              for cat in db_categories}, response['categories'])
        self.assertEqual(len(db_categories), response['total_categories'])

    def test_02_get_questions(self):
        response = self.json('/questions')

        self.assertEqual(response['success'], True)
        self.assertListEqual(list(response.keys()), [
                             'categories', 'current_category', 'questions', 'success', 'total_questions'])
        self.assertTrue(isinstance(response['questions'], list))
        self.assertDictEqual({str(cat.id): cat.type
                              for cat in db_categories}, response['categories'])
        self.assertEqual(response['total_questions'], db_questions_count)

    def test_03_not_found_questions_page(self):

        response = self.json('/questions?page=1000')

        self.assertFalse(response['success'])
        self.assertTrue('message' in response.keys())
        self.assertEqual(response['error'], 404)

    """
    test create question endpint first to use the created question in
    testing search questions endpoint and then delete question endpoint
    """

    def test_04_create_new_question(self):

        new_question = {
            'question': 'test question ?',
            'answer': 'answer',
            'category': db_categories[0].id,
            'difficulty': 4
        }

        before_create_count = db_questions_count

        self.client().post('questions', data=json.dumps(new_question),
                           content_type='application/json')

        global last_questions_count
        after_create_count = last_questions_count = Question.query.count()

        self.assertEqual(before_create_count + 1, after_create_count)

        db_new_question = Question.query.order_by(
            Question.id.desc()).first().format()

        global inserted_question
        inserted_question = db_new_question.copy()

        db_new_question.pop('id')

        self.assertDictEqual(db_new_question, new_question)

    def test_05_create_new_question_missing_data(self):

        new_question = {
            'question': 'test question ?',
            'category': db_categories[0].id,
            'difficulty': 4
        }

        response = json.loads(self.client().post('questions', data=json.dumps(new_question),
                                                 content_type='application/json').data)

        self.assertFalse(response['success'])
        self.assertTrue('message' in response.keys())
        self.assertEqual(response['error'], 400)

    def test_06_search_questions(self):

        response = json.loads(self.client().post(
            '/search-questions', data=json.dumps({'searchTerm': inserted_question['question'][0:7]}),
            content_type='application/json').data)

        self.assertTrue(response['success'])

        db_search = Question.query.filter(Question.question.ilike(
            '%' + inserted_question['question'][0:7] + '%')).all()

        if len(db_search) >= 10:
            self.assertEqual(len(response['questions']), 10)
        else:
            self.assertEqual(len(response['questions']), len(db_search))

        self.assertEqual(response['total_questions'], len(db_search))
        self.assertDictEqual({str(cat.id): cat.type
                              for cat in db_categories}, response['categories'])

    def test_07_search_not_found(self):
        response = json.loads(self.client().post(
            '/search-questions', data=json.dumps({'searchTerm': 'any term that absolutley will not be found in questions'}),
            content_type='application/json').data)

        self.assertFalse(response['success'])
        self.assertTrue('message' in response.keys())
        self.assertEqual(response['error'], 404)

    def test_08_delete_question(self):

        global last_questions_count
        before_delete_count = last_questions_count

        response = json.loads(self.client().delete(
            '/questions/' + str(inserted_question['id']),
            content_type='application/json').data)

        after_delete_count = last_questions_count = Question.query.count()

        self.assertTrue(response['success'])
        self.assertEqual(before_delete_count - 1, after_delete_count)
        self.assertIsNone(Question.query.get(inserted_question['id']))

    def test_09_delete_question_not_found(self):
        response = json.loads(self.client().delete(
            '/questions/1000',
            content_type='application/json').data)

        self.assertFalse(response['success'])
        self.assertTrue('message' in response.keys())
        self.assertEqual(response['error'], 404)

    def test_10_get_by_category(self):
        choosen_category = random.choice(db_categories).format()

        response = self.json(
            '/categories/' + str(choosen_category['id']) + '/questions')

        self.assertEqual(response['success'], True)
        self.assertListEqual(list(response.keys()), [
                             'categories', 'current_category', 'questions', 'success', 'total_questions'])
        self.assertTrue(isinstance(response['questions'], list))
        self.assertDictEqual({str(cat.id): cat.type
                              for cat in db_categories}, response['categories'])
        self.assertEqual(response['total_questions'], Question.query.filter(
            Question.category == choosen_category['id']).count())

    def test_11_not_found_questions_in_category(self):

        response = self.json('/categories/1000/questions')

        self.assertFalse(response['success'])
        self.assertTrue('message' in response.keys())
        self.assertEqual(response['error'], 404)

    def test_12_quizzes(self):
        available_questions = 5 if last_questions_count > 5 else last_questions_count
        previous_questions = []

        while len(previous_questions) < available_questions:
            response = json.loads(self.client().post('/quizzes', data=json.dumps({
                'quiz_category': {'id': 0},  # means all categories
                'previous_questions': previous_questions
            }), content_type='application/json').data)

            self.assertTrue(response['success'])

            previous_questions.append(response['question']['id'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
