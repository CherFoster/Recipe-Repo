from flask import request, make_response, session, jsonify, abort
from flask_restful import Resource
from config import app, db, api
from models import User, Recipe, Cuisine

@app.route('/')
def index():
    return '<h1>Phase 4 Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

