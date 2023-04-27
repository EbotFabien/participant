from flask import Flask, render_template, url_for,flash,redirect,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import  LoginManager
#from flask_mail import Mail
from app.config import Config
import os
from firebase_admin import credentials, firestore, initialize_app
# Initialize Flask App

# Initialize Firestore DB



cred = credentials.Certificate('app/participant.json')
default_app = initialize_app(cred)
db = firestore.client()
bcrypt = Bcrypt()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

   
    bcrypt.init_app(app)
   

    from app.entity.users.routes import users
    from app.entity.agentc.routes import agentcon
    from app.entity.mandataire.routes import mandataire
    from app.entity.locataire.routes import locataire
    from app.entity.bailleur.routes import bailleur
    from app.entity.client.routes import client
    from app.entity.donneurd.routes import donneur
    from app.entity.prop.routes import prop
    
    app.register_blueprint(users)
    app.register_blueprint(agentcon)
    app.register_blueprint(mandataire)
    app.register_blueprint(locataire)
    app.register_blueprint(bailleur)
    app.register_blueprint(client)
    app.register_blueprint(donneur)
    app.register_blueprint(prop)
    


    return app