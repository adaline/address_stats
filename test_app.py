# coding: utf-8
import pytest

from test.support.configure_test import app
from app import db
from config import TestingConfig


def test_db_create(app):
    app = app(TestingConfig)

    test_model_to_insert = model1.Model1(
        cool_field="test name", cooler_field="Cooler String"
    )
    test_model_to_insert.save()
    db.session.commit()

    assert db.session.query(model1.Model1).one()


class TestAddresses:

    def test_get_count(self):
        resp = app.get('/count')
        assert resp.status_int == 200
        assert resp.json['profile']['email'] == 'foo@bar.com'

    def test_get_count_with_postcodes(self, app):
        resp = app.get('/count/10969;10997')
        assert resp.status_int == 200
        assert resp.json['profile']['email'] == 'foo@bar.com'

    def test_get_distribution(self, app):
        resp = app.get('/distribution')
        assert resp.status_int == 200
        assert resp.json['profile']['email'] == 'foo@bar.com'

    def test_get_distribution_with_postcodes(self, app):
        resp = app.get('/distribution/10969;10997')
        assert resp.status_int == 200
        assert resp.json['profile']['email'] == 'foo@bar.com'
