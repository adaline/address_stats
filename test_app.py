# coding: utf-8
import pytest
import json
import os
from datetime import datetime

from app import app, db, Address


@pytest.fixture
def client():
    app.config.from_object('config.TestConfig')

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_get_root(client):
    respoonse = client.get('/')
    assert respoonse.status_code == 200
    assert respoonse.data.decode('utf8') == 'Welcome to address stats API'


def test_get_count(client):
    # 2 entries
    db.session.add(Address(id=1, postcode=10997, added_on=datetime.now()))
    db.session.add(Address(id=2, postcode=10997, added_on=datetime.now()))
    db.session.commit()

    respoonse = client.get('/count', follow_redirects=True)
    assert respoonse.status_code == 200

    # We get 2 as a result
    assert json.loads(respoonse.data.decode('utf8')) == {"count": 2}


def test_get_count_with_postcodes(client):
    # 3 entries we want, 1 we dont
    db.session.add(Address(id=1, postcode=10997, added_on=datetime.now()))
    db.session.add(Address(id=2, postcode=10997, added_on=datetime.now()))
    db.session.add(Address(id=3, postcode=10969, added_on=datetime.now()))
    db.session.add(Address(id=4, postcode=10007, added_on=datetime.now()))
    db.session.commit()

    respoonse = client.get('/count/10969;10997', follow_redirects=True)
    assert respoonse.status_code == 200

    # We get 3 as a result
    assert json.loads(respoonse.data.decode('utf8')) == {"count": 3}


def test_get_distribution(client):
    db.session.add(Address(id=1, postcode=10997,
                           added_on=datetime(2012, 3, 16, 1, 0)))
    db.session.add(Address(id=2, postcode=10997,
                           added_on=datetime(2012, 3, 16, 1, 0)))
    db.session.add(Address(id=3, postcode=10969,
                           added_on=datetime(2014, 3, 16, 1, 0)))
    db.session.add(Address(id=4, postcode=10007,
                           added_on=datetime(2016, 3, 16, 1, 0)))
    db.session.commit()

    respoonse = client.get('/distribution', follow_redirects=True)
    assert respoonse.status_code == 200

    # We get distribution of all entries
    assert json.loads(respoonse.data.decode('utf8')) == [
        {"2012": 2}, {"2014": 1}, {"2016": 1}]


def test_get_distribution_with_postcodes(client):
  # 3 entries we want, 1 we dont
    db.session.add(Address(id=1, postcode=10997,
                           added_on=datetime(2012, 3, 16, 1, 0)))
    db.session.add(Address(id=2, postcode=10997,
                           added_on=datetime(2012, 3, 16, 1, 0)))
    db.session.add(Address(id=3, postcode=10969,
                           added_on=datetime(2014, 3, 16, 1, 0)))
    db.session.add(Address(id=4, postcode=10007,
                           added_on=datetime(2016, 3, 16, 1, 0)))
    db.session.commit()

    respoonse = client.get('/distribution/10969;10997', follow_redirects=True)
    assert respoonse.status_code == 200

    # We get distribution of the entries in the postcodes
    assert json.loads(respoonse.data.decode('utf8')) == [
        {"2012": 2}, {"2014": 1}]
