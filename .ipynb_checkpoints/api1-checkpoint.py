from flask import Flask, jsonify, render_template
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
import json

# Ces 2 lignes doivent toujours exister en haut du code pour initialiser l'app flask et l'API.
app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
    return "Hello World"


@app.route("/banknotes/")
def banknotes():
    return render_template('banknotes.html')
#"Bienvenue sur l'analyse de <i>billets</i>"


if __name__ == '__main__':
    # Load model
    #with open('model.pickle', 'rb') as f:
     #   model_reg_log = pickle.load(f)
    # launch server in debug mode
    app.run(debug=True)