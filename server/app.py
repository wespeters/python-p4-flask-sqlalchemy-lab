#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    if animal is None:
        return make_response("<h1>Error: Animal not found</h1>", 404)

    response = f"""
    <ul>Name: {animal.name}</ul>
    <ul>Species: {animal.species}</ul>
    <ul>Zookeeper: {animal.zookeeper.name if animal.zookeeper else 'None'}</ul>
    <ul>Enclosure: {animal.enclosure.environment if animal.enclosure else 'None'}</ul>
    """

    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    if zookeeper is None:
        return make_response("<h1>Error: Zookeeper not found</h1>", 404)

    response = f"""
    <ul>Name: {zookeeper.name}</ul>
    <ul>Birthday: {zookeeper.birthday.isoformat()}</ul>
    <ul>Animals: {', '.join([animal.name for animal in zookeeper.animals])}</ul>
    """

    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    if enclosure is None:
        return make_response("<h1>Error: Enclosure not found</h1>", 404)

    response = f"""
    <ul>Environment: {enclosure.environment}</ul>
    <ul>Open to visitors: {'Yes' if enclosure.open_to_visitors else 'No'}</ul>
    <ul>Animals: {', '.join([animal.name for animal in enclosure.animals])}</ul>
    """

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
