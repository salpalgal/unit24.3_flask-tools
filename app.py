from flask import Flask , render_template , request , redirect ,flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config["SECRET_KEY"]="HELLO"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
responses = [""]
surveys_obj = surveys.surveys
satisfaction_questions = surveys_obj["satisfaction"].questions

@app.route("/")
def start():
    satisfaction_title = surveys_obj["satisfaction"].title
    satisfaction_instructions = surveys_obj["satisfaction"].instructions
    return render_template("homepage.html" , satisfaction_title = satisfaction_title, satisfaction_ins = satisfaction_instructions)

@app.route("/answers", methods = ["POST"])
def answers():
    ans = request.form["answer"]
    responses.append(ans)
    if len(responses) <= len(satisfaction_questions):
        num = len(responses)
    else:
        num = "done"
    return redirect(f"/questions/{num}")

@app.route("/questions/<num>")
def question(num):
    question_num = int(num)-1
    next_num = int(len(responses))
    current_num = int(num)
    if current_num != next_num or  question_num > len(satisfaction_questions):
        flash("invalid question !")
        return redirect(f"/questions/{next_num}")
    else: 
        q = satisfaction_questions[question_num].question
        choices = satisfaction_questions[question_num].choices
        return render_template("questions.html",question = q ,choices = choices ,num = num)

@app.route("/questions/done")
def thanks():
    return render_template("done.html")