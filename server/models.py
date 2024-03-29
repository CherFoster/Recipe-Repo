from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

recipe_cuisines = db.Table('recipe_cuisines', 
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
    db.Column('cuisine_id', db.Integer, db.ForeignKey('cuisines.id'))
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

    recipes = db.relationship('Recipe', back_populates='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')
    
    # Takes password, hashes it, and stores the hash
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    # compares hashed password to the stored hash  
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'
    
class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    ingredients = db.Column(db.String)
    instructions = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='recipes')
    cuisines = db.relationship('Cuisine', secondary=recipe_cuisines, back_populates='recipes')

    def __repr__(self):
        return (
            f'Name: {self.name}, ' \
            + f'Image: {self.image},' \
            + f'Ingredients: {self.ingredients},' \
            + f'Instructions: {self.instructions},' \
        )
    
class Cuisine(db.Model, SerializerMixin):
    __tablename__ = 'cuisines'

    id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.String)

    recipes = db.relationship('Recipe', secondary=recipe_cuisines, back_populates='cuisines')

    def __repr__(self):
        return f'<Cuisine {self.cuisine}>'
