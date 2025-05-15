from flask import Flask, render_template, make_response, url_for
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'       # e.g., 'root'
app.config['MYSQL_PASSWORD'] = 'MitManav@4703'
app.config['MYSQL_DB'] = 'flask_db'




@app.route('/')
def home_page():
    fruit_list = ["apple", "Banana", "Cherry"]
    msg = "<h1>My name is <strong>Manav</strong></h1>"
    html_content = render_template("homePage.html",
                                    fruit_list = fruit_list,
                                    msg=msg ) 
    response = make_response(html_content);
    return response;
@app.route('/market')
def market_page():
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