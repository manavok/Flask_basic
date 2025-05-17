from flask import Flask, render_template, make_response, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)

app.config["SECRET_KEY"] = 'Krnsa'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'       # e.g., 'root'
app.config['MYSQL_PASSWORD'] = 'MitManav@4703'
app.config['MYSQL_DB'] = 'flask_db'

class Myform(FlaskForm):
    name = StringField("Name: ",
                       validators=[DataRequired(), Length(min = 3, max=10)],
                       render_kw = {'class': 'text-2xl'});
    email = EmailField("Email: ",
                        validators=[DataRequired(),Email()],
                        render_kw={'class' : 'input input-primary h-8', 'placeholder': 'abc123@gmail.com', 'type': 'email'})
    submit = SubmitField("Submit")
    

@app.route('/')
def home_page():
    flash("Welcom To My Page, Hare Krsna!")
    fruit_list = ["apple", "Banana", "Cherry"]
    msg = "<h1>My name is <strong>Manav</strong></h1>"
    html_content = render_template("homePage.html",
                                    fruit_list = fruit_list,
                                    msg=msg ) 
    response = make_response(html_content);
    return response;
@app.route('/market')
def market_page():
    flash("Welcom to my market")
    fruit_list = ["apple", "Banana", "Cherry"]
    response = make_response(render_template("marketPage.html", fruit_list = fruit_list))
    return response

# page not found
@app.errorhandler(404)
def not_found_error(error):
    html_content = render_template("404.html")
    response = make_response(html_content)
    response.status_code = 404
    return response

#internal server error
@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

@app.route('/form', methods = ["GET", "POST"])
def form_page():
    name = None
    form = Myform()
    # validate form
    if form.validate_on_submit(): # if submit succcessful=>return true
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Sucessfully!!")
    
    return render_template('form.html',
                           name = name,
                           form = form)