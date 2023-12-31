#---------------------APP PREP: Accessing FLASK, TOOLBAR, and JINJA----------------
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
app = Flask(__name__)
app.config['SECRET_KEY'] = 'candy-apple'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
#----------------------------------------------------------------------------------
responses = []
total_questions = 0
for question in survey.questions:
    total_questions += 1
questions = [survey.questions]


@app.route("/")
def home_page():
    """Shows home page of survey app"""
    title = survey.title
    instructions = survey.instructions
    
    return render_template('homepage.html', title = title, instructions = instructions)

@app.route("/start")
def start_survey():
    """Directs user to the survey questions"""
    return redirect("/questions/0")

@app.route('/answer', methods = ["POST"])
def handle_submissions():
    '''Adds answers to responses. Redirects user to the next question'''
    choice = request.form['answer']
    responses.append(choice)
    total_answered = len(responses)
    next_question = len(responses)
    if (total_answered == total_questions):
        return redirect("/thanks")
    else:
        return redirect(f"questions/{next_question}")


@app.route("/questions/<int:num>")
def show_question(num):
    '''Provides questions'''
    
    total_answered = len(responses)
    next_question = len(responses)
    if (responses is None):
        # Sends user to homepage if the user tries to manually go to a question before survey starts
        return redirect("/")

    if total_answered == total_questions:
        # Survey is over. Sends user to thank-you page. 
        return redirect('/thanks')
    
    if (total_answered != num):
        # Trying to access questions out of order.
        flash(f"You do not currently have access to Question #{num}. Please answer Question #{next_question +1}.")
        return redirect(f"/questions/{next_question}")
    
    UI_question = num + 1
    q_num = total_answered
    question = survey.questions[num].question
    choices = survey.questions[num].choices
    return render_template('questions.html', choices = choices, question = question, UI_question = UI_question,total= total_questions)

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', responses = responses)