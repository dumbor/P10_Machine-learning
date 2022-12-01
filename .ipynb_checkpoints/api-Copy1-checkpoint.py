from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
import json
import pandas as pd


# Ces 2 lignes doivent toujours exister en haut du code pour initialiser l'app flask et l'API.
# Instanciation de Flask
app = Flask(__name__)

# Création de l'instance API
api = Api(app)

# prediction API call (utilisation de la méthode Resource)
class prediction(Resource):
    def get(self, diagonal,height_left,height_right,margin_low,margin_up,length): #banknotes = my csv file
        print(banknotes) # to delete after test
        df=pd.DataFrame(banknotes,columns=['Prédiction'])

        # Load model
        model = pickle.load(open('model.pickle', 'rb'))
        # Access the predict function from the model
        prediction = model.predict(df) # c'est mon fichier en entrée
        return(prediction) 

# Creating endpoint
api.add_resource(prediction, '/prediction/')  # respond to a get request

# To serve the data to web application, we create another class
class getData(Resource):
    def get(self):
        prod_banknotes = pd.read_csv("Fichiers/billets_production.csv", sep=",")
        res = prod_banknotes.to_json(orient = "records") #returning json from this class
        return res
    
# mapping the class to an endpoint
api.add_resource(getData, '/api')  

if __name__ == '__main__':
    # launch server in debug mode
    app.run(debug=True)
