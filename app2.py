# for database practice
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 
import sqlite3,os
from flask_migrate import Migrate

app = Flask(__name__)
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User = User, Role = Role)

# for flask-sqlalchemy:
# MySQL: mysql://username:password@hostname/database
# PostgreSQL: postgresql://username:password@hostname/database
# SQLite: sqlite:///c:/absolute/path/to/database

# sqlite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database2.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)

    users = db.relationship('User', backref = 'role', lazy = "dynamic")

    def __repr__(self):
        return f"Role: {self.name}"
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f"User: {self.username}"

@app.route
def home_page():
    return render_template('homePage2.html')


    
if __name__ == '__main__':
    app.run(debug=True)