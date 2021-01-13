import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random, secrets
from models import setup_db, Question, Category

# this is used in common function for number of records per page
QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy(app)
  
  ''' COMPLETED 
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  #if we have to do resource specific usage then following can be uncommented in future:
  #CORS(app, resources={r"/api/*": {"origins": "*"}})

  CORS(app)

  ''' COMPLETED 
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

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

  '''
  @TODO: COMPLETED 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/hello', methods=['GET','POST'])
  def get_greeting():
    return jsonify({'message':'Hello, World!'})


  '''
  @TODO: COMPLETED 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/categories', methods=['GET'])
  def get_categories():
    try:
      page = request.args.get('page', 1, type=int)
      start = (page -1) * 10
      end   = start + 10
      categories = Category.query.all()
      formatted_categories = {category.id: category.type for category in categories}
      return jsonify({
          'success': True,
          'categories': formatted_categories,
      })
    
    except:
      abort(400)

  @app.route('/questions', methods=['GET'])
  def get_questions():

    try:

      questions = Question.query.all()
      categories = Category.query.all()

      formatted_categories = {category.id: category.type for category in categories}

      current_questions = paginate_questions(request, questions)

      print(len(questions))

      if len(current_questions) ==0:
        abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(questions),
        'categories': formatted_categories,
        'current_category': None
      })

    except:
      abort(404)

  '''
  @TODO: COMPLETED
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    try:

      print('inside delete block')

      question = Question.query.filter(Question.id == question_id).one_or_none()
      question.delete()

      #load everything back
      questions = Question.query.all()
      categories = Category.query.all()

      current_questions = paginate_questions(request, questions)

      if len(current_questions) ==0:
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

    except:
      abort(422)

  '''
  @TODO: COMPLETED
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def insert_question():

    print('inside question post method')
    requestPayload = request.get_json()
    print(requestPayload)
    newQuestionVal = requestPayload.get('question','')
    newAnswerVal = requestPayload.get('answer','')
    newDifficultyVal = requestPayload.get('difficulty','')
    newCategoryVal = requestPayload.get('category','')

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

    except:
      abort(422)

  '''
  @TODO: COMPLETED 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST','GET'])
  def search_questions():

    # query: http://127.0.0.1:5000/questions/search?search_term=soccer
    # print('testing query params')
    # f = furl("/abc?def='ghi'") 
    # print(f.args['def'])

    # GET URL testing
    #search_term = request.args.get('search_term', '')

    # POST testing
    requestPayload = request.get_json()
    print(requestPayload)
    search_term = requestPayload.get('searchTerm','')
    print('Search term is ' + search_term)
    search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    print('processed data is')
    print(len(search_results)) 

    current_questions = paginate_questions(request, search_results)

    if len(current_questions) ==0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(current_questions)
    })

  '''
  @TODO: COMPLETED 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def show_questions(category_id):

    search_results = Question.query.filter(Question.category == category_id).all()
    print('processed data is')
    print(len(search_results)) 

    current_questions = paginate_questions(request, search_results)

    if len(current_questions) ==0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(current_questions)
    })


  '''
  @TODO: COMPLETED
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

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
      quizQuestions = Question.query.filter_by(category = quiz_category['id']).all()
    
    print(quizQuestions)

    data = []

    for question in quizQuestions:
      if question.id not in previous_questions:
        data.append(question.format())

    questionRecord = ''
    #print(random.choice(data))
    #print(secrets.choice(data))

    if len(data) != 0:
      questionRecord = secrets.choice(data)

    return jsonify({
      'success': True,
      'question': questionRecord
    })

  '''
  @TODO: COMPLETED
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

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
