import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = ( page - 1 ) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [ question.format() for question in selection ]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Controll-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  
  

  

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    selection = Category.query.all()
    categories = {}
    for category in selection:
      categories[str(category.id)] = category.type
    return jsonify({
      'success':True, 
      'categories':categories
      })
    


  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    if len(current_questions) == 0:
      abort(404)
    selection = Category.query.all()
    categories = {}
    for category in selection:
      categories[str(category.id)] = category.type
    return jsonify({
      'success': True,
      'questions': current_questions,
      'totalQuestions': len(Question.query.all()),
      'categories': categories,
      'currentCategory': ''
      })

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)
      question.delete()
      
      return jsonify({'success':True})
    except:
      abort(422)




  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    request_data = request.get_json()
    if request_data is None:
        abort(400)
    try:
      if 'question' not in request_data:
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(request_data.get('searchTerm', None))))
        questions = [question.format() for question in selection]
        return jsonify({
          'success': True,
          'questions': questions,
          'totalQuestions': len(questions),
          'currentCategory': ''
        })
      else:
        new_question = request_data.get('question')
        new_answer = request_data.get('answer')
        new_difficulty = request_data.get('difficulty')
        new_category = request_data.get('category')
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()
        return jsonify({'success':True})
    except:
      abort(422)
    

  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    selection = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
    questions = [question.format() for question in selection]
    if len(questions) == 0:
      abort(404)
    
    category = Category.query.filter(Category.id == category_id).one_or_none()
    return jsonify({
      'success': True,
      'questions': questions,
      'totalQuestions': len(Question.query.all()),
      'currentCategory': category.type
      })

  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    try:
      request_data = request.get_json()
      category_id = request_data.get('quiz_category')['id']
      previous_qs = request_data.get('previous_questions')
      selection = Question.query.filter(Question.category == category_id).filter(~Question.id.in_(previous_qs)).first()
      question = None
      if selection is not None:
        question = selection.format()  
      return jsonify({
        'success': True,
        'question': question
      })
      
    except:
      abort(400)


  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422
  
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  
  @app.errorhandler(500)
  def interal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500
  
  return app

    