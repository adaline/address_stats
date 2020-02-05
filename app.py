from werkzeug.routing import BaseConverter
import os
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property


# Config

app = Flask(__name__)
app.config.from_object(
    os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))

db = SQLAlchemy(app)


# We need a custom URL converter to pass multiple postocdes

class IntListConverter(BaseConverter):
    """Match ints separated with ';'."""

    # at least one int, separated by ;, with optional trailing ;
    regex = r'\d+(?:;\d+)*;?'

    # this is used to parse the url and pass the list to the view function
    def to_python(self, value):
        return [int(x) for x in value.split(';')]

    # this is used when building a url with url_for
    def to_url(self, value):
        return ';'.join(str(x) for x in value)


app.url_map.converters['int_list'] = IntListConverter


# Model

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postcode = db.Column(db.Integer, nullable=False, index=True)
    added_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Address %r>' % self.id

# Endpoints


@app.route('/')
def index():
    return "Welcome to address stats API"


# An endpoint that delivers the number of buildings per zip code
@app.route('/count/', defaults={'postcodes': None})
@app.route('/count/<int_list:postcodes>')
def count(postcodes):
    if postcodes != None:
        # Postocdes given?
        count_results = db.session.execute(
            db.session.query(Address)
            .filter(Address.postcode.in_(postcodes))
            .statement.with_only_columns([db.func.count()]).order_by(None)
        ).scalar()
    else:
        # No postocdes, show everything
        count_results = db.session.query(Address).count()

    return app.response_class(
        response=json.dumps({'count': count_results}),
        status=200,
        mimetype='application/json'
    )


# An endpoint that shows the distribution of years in which buildings were added to the dataset
@app.route('/distibution/', defaults={'postcodes': None})
@app.route('/distibution/<int_list:postcodes>')
def distibution(postcodes):
  # SQLite's way of grabbing a year from datetime
    year_func = db.func.strftime('%Y', Address.added_on)

    if postcodes != None:
        # Postocdes given?
        distribution_results = db.session.execute(
            db.select([year_func, db.func.count(year_func)])
            .where(Address.postcode.in_(postcodes))
            .group_by(year_func)
            .order_by(year_func)
        )
    else:
        # No postocdes, show everything
        distribution_results = db.session.execute(
            db.select([year_func, db.func.count(year_func)])
            .group_by(year_func)
            .order_by(year_func)
        )

    # Map into correct structure for serialization
    response = [{rowproxy['strftime_1']: rowproxy['count_1']}
                for rowproxy in distribution_results]

    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run()
