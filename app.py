from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.sqlite'
db = SQLAlchemy(app)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.Integer, nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False)


@app.route('/')
def index():
    return "Welcome to address stats API"


if __name__ == "__main__":
    app.run(debug=True)
