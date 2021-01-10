import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def all_categories():
        cats = {cat.id: cat.type
                for cat in Category.query.all()}
        return jsonify({
            'success': True,
            'categories': cats,
            'total_categories': len(cats)
        })

    @app.route('/questions', methods=['GET'])
    def questions():
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {cat.id: cat.type
                           for cat in Category.query.all()},
            'current_category': None
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            question.delete()

            return jsonify({
                'success': True
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def new_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)

        if(None in [question, answer, difficulty, category]):
            abort(400)

        try:
            question_to_add = Question(
                question=question, answer=answer, difficulty=difficulty, category=category)
            question_to_add.insert()

            return jsonify({
                'success': True
            })
        except:
            abort(422)

    @app.route('/search-questions', methods=['POST', 'GET'])
    def search_questions():
        try:
            search_term = request.get_json().get('searchTerm')
            selection = Question.query.filter(
                Question.question.ilike('%' + search_term + '%')).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }), 404

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': {cat.id: cat.type
                               for cat in Category.query.all()},
                'current_category': None
            })
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_by_category(category_id):
        selection = Question.query.filter(
            Question.category == category_id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {cat.id: cat.type
                           for cat in categories},
            'current_category': [cat.format()
                                 for cat in categories if cat.id == category_id][0]
        })

    @app.route('/quizzes', methods=['POST'])
    def quizzes():
        body = request.get_json()

        category_id = body.get('quiz_category').get('id')
        previous = body.get('previous_questions')

        try:
            questions = Question.query.filter(~Question.id.in_(previous))

            if(category_id >= 1):
                questions = questions.filter(
                    Question.category == category_id)

            questions = questions.all()

            return jsonify({
                'success': True,
                'question': random.choice(questions).format() if len(questions) else False
            })

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
