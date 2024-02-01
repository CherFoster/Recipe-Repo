from random import randint, choice as rc
from faker import Faker
from app import app
from config import db
from models import User, Recipe, Cuisine

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
