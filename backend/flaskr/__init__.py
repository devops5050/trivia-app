import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import secrets
from models import setup_db, Question, Category

# this is used in common function for number of records per page
QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)

    # if we have to do resource specific usage then
    # following can be uncommented in future:
    # CORS(app, resources={r"/api/*": {"origins": "*"}})

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # helper method from error handling intro video
    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/hello', methods=['GET', 'POST'])
    def get_greeting():
        return jsonify({'message': 'Hello, World!'})

    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10
            categories = Category.query.all()
            formatted_categories = {category.id: category.type for category in categories}
            return jsonify({
                'success': True,
                'categories': formatted_categories,
            })

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/questions', methods=['GET'])
    def get_questions():

        try:
            questions = Question.query.all()
            categories = Category.query.all()

            formatted_categories = {category.id: category.type for category in categories}

            current_questions = paginate_questions(request, questions)

            print(len(questions))

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
              'success': True,
              'questions': current_questions,
              'total_questions': len(questions),
              'categories': formatted_categories,
              'current_category': None
            })

        except Exception as e:
            print(e)
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            print('inside delete block')

            question = Question.query.filter(Question.id == question_id).one_or_none()
            question.delete()

            # load everything back
            questions = Question.query.all()
            categories = Category.query.all()

            current_questions = paginate_questions(request, questions)

            if len(current_questions) == 0:
                abort(404)

            formatted_categories = {category.id: category.type for category in categories}

            return jsonify({
              'success': True,
              'deleted': question_id,
              'questions': current_questions,
              'total_questions': len(questions),
              'categories': formatted_categories,
              'current_category': None
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions', methods=['POST'])
    def insert_question():

        print('inside question post method')
        requestPayload = request.get_json()
        print(requestPayload)
        newQuestionVal = requestPayload.get('question', '')
        newAnswerVal = requestPayload.get('answer', '')
        newDifficultyVal = requestPayload.get('difficulty', '')
        newCategoryVal = requestPayload.get('category', '')

        try:
            question = Question(question=newQuestionVal, answer=newAnswerVal, category=newCategoryVal, difficulty=newDifficultyVal)
            question.insert()

            newresultset = Question.query.order_by(Question.id).all()
            new_questions = paginate_questions(request, newresultset)

            return jsonify({
              'success': True,
              'created': question.id,
              'questions': new_questions,
              'total_questions': len(Question.query.all())
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions/search', methods=['POST', 'GET'])
    def search_questions():

        # query: http://127.0.0.1:5000/questions/search?search_term=soccer
        # print('testing query params')
        # f = furl("/abc?def='ghi'")
        # print(f.args['def'])

        # GET URL testing
        # search_term = request.args.get('search_term', '')

        # POST testing
        requestPayload = request.get_json()
        print(requestPayload)
        search_term = requestPayload.get('searchTerm', '')
        print('Search term is ' + search_term)
        search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        print('processed data is')
        print(len(search_results))

        current_questions = paginate_questions(request, search_results)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(current_questions)
        })

    @app.route('/categories/<category_id>/questions')
    def show_questions(category_id):

        search_results = Question.query.filter(Question.category == category_id).all()
        print('processed data is')
        print(len(search_results))

        current_questions = paginate_questions(request, search_results)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(current_questions)
        })

    @app.route('/quizzes', methods=['POST'])
    def quizzes():

        print('inside question post method')
        requestPayload = request.get_json()
        print(requestPayload)
        # {
        #   'previous_questions': [],
        #   'quiz_category': {'type': 'click', 'id': 0}
        # }

        previous_questions = requestPayload.get('previous_questions', [])
        quiz_category = requestPayload.get('quiz_category', '')

        print('previous_questions total: ' + str(len(previous_questions)))
        print('quiz_category: ' + str(quiz_category['id']))

        if quiz_category['id'] == 0:
            quizQuestions = Question.query.all()
        else:
            quizQuestions = Question.query.filter_by(category == quiz_category['id']).all()

        print(quizQuestions)

        data = []

        for question in quizQuestions:
            if question.id not in previous_questions:
                data.append(question.format())

        questionRecord = ''
        # print(random.choice(data))
        # print(secrets.choice(data))

        if len(data) != 0:
            questionRecord = secrets.choice(data)

        return jsonify({
          'success': True,
          'question': questionRecord
        })

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
          'success': False,
          'error': 400,
          'message': 'Invalid Request Message'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          'success': False,
          'error': 404,
          'message': 'Resource Not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
        }), 422


    return app
