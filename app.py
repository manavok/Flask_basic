from flask import Flask, render_template, make_response, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config
import mysql.connector
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
# MySQL
app.config.from_object(Config)

# to work with UTC
moment = Moment(app)

# add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDataBase.db'
# secret key
app.config["SECRET_KEY"] = "Hare Krsna"

# initialize database
db = SQLAlchemy(app)
# flask-sqlAlchemy- defining model
class dataBase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(20), nullable = False, unique=True)
    date_add = db.Column(db.DateTime, default = datetime.now())

    # Create a string
    def __repr__(self):
        return f"<name { self.name }>"
        


# Flask-Form
class Myform(FlaskForm):
    name = StringField("Name: ",
                       validators=[DataRequired(), Length(min = 3, max=20)],
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
                                    msg=msg,
                                    current_time = datetime.utcnow()  ) 
    response = make_response(html_content);
    flash("Flash Message, Hare Krsna!")
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

# #internal server error
# @app.errorhandler(500)
# def server_error(error):
#     return render_template('500.html'), 500

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

@app.route('/add/dataBase', methods=['GET','POST'])
def use_database():
    form = Myform()
    is_same_email = False
    if form.validate_on_submit():
        # check email exist or not
        existing_email = dataBase.query.filter_by(email = form.email.data).first()

        if existing_email:
            flash("Email Already Exist", category='error')
            is_same_email = True
        else:
        # 1. Create a new row in database
            new_data = dataBase(name = form.name.data, email = form.email.data )
        # 2. Add and save it in database
            db.session.add(new_data)
            db.session.commit()

        # clear form data after submission
            form.name.data = ''
            form.email.data = ''

            flash("Form submitted Successfully!", category='success')

    all_data = dataBase.query.order_by(dataBase.date_add.desc()).all()
    return render_template('dataBaseUse.html',
                           form = form,
                           all_data = all_data,
                        is_same_email = is_same_email )

@app.route('/delete/<int:id>', methods=["Post"])
def delete_data(id):
    delete_row = dataBase.query.get_or_404(id) # get that row. If row not exist->return 404 error
    db.session.delete(delete_row)
    db.session.commit()
    flash("❌ Entry deleted successfully!", category= 'delete')
    return redirect(url_for("use_database"))

if __name__ == '__main__':
    app.run(debug=True)