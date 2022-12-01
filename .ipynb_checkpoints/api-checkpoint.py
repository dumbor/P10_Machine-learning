from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import pickle
import numpy as np
import json


# Ces 2 lignes doivent toujours exister en haut du code pour initialiser l'app flask et l'API.
app = Flask(__name__)
api = Api(app)

# Le bloc de code ci-dessus crée un analyseur de requête pour parser les arguments qui seront envoyés avec la requête.
# Dans notre cas, puisque nous fournissons le modèle ML, nous envoyons généralement les données dans un format sérialisé JSON et nommons la clé 'data' : nous demandons donc à l'analyseur de rechercher les données contenues dans la requête.

# Create parser for the payload data
parser = reqparse.RequestParser()
parser.add_argument('data')

# Ensuite, nous créons une classe appelée BankNoteClassifier en héritant de la classe Resource que nous avons importée de flask-restful, qui définit déjà diverses méthodes de gestion de différents types de # requêtes, notamment get, post, ,put, ,delete, etc. Notre objectif est de réécrire la méthode post et de lui dire comment utiliser le modèle pour faire des prédictions sur les données fournies. 

# Étant donné que le but de notre API est de servir des modèles ML, nous n'avons besoin que de la méthode post et ne nous soucions pas des autres.<br>

# Dans la méthode post, nous appelons d'abord l'analyseur qu'on vient de définir pour obtenir les arguments. Les données (à l'origine np.array) sont sérialisées au format chaîne dans le JSON, nous utilisons donc $json.loads$ pour les désérialiser dans une liste, puis de nouveau dans un tableau NumPy. <br>
# La partie prédiction reste la même que celle des modèles scikit-learn.

# Dans la dernière étape, nous devons remettre les étiquettes prédites (np.array) dans la liste et appeler la fonction jsonify importée de flask pour la sérialiser à nouveau afin qu'elles soient renvoyées à l'application dans un format approprié.

# Une fois la classe définie, nous ajoutons notre classifieur (essentiellement une classe de ressources modifiée) dans notre API, ainsi que la route relative pour y accéder, dans notre cas c'est /banknotes.<br>
# L'URL complète de notre modèle ML sera alors quelque chose comme http://127.0.0.1:5000/banknotes si nous exécutons localement.

# Define how the api will respond to the post requests
class BankNoteClassifier(Resource):
    def post(self):
        args = parser.parse_args()
        X = np.array(json.loads(args['data']))
        prediction = model_reg_log.predict(X)
        return jsonify(prediction.tolist())

api.add_resource(BankNoteClassifier, '/banknotes')


# Je créé un message sur la page d'accueil
@app.route("/")
def hello():
    return "Bienvenue sur l'url de test de l'authenticité des billets -> <a href = http://localhost:5000/banknotes>ici</a>"

# Dans la dernière partie du code dans api.py, nous chargeons le modèle enregistré à partir de la dernière section afin que l'application sache où obtenir le modèle si une prédiction est demandée.<br>
# Ensuite, nous exécutons l'application flask en mode débogage, où elle permet simplement d'exécuter du code arbitraire directement dans le navigateur en cas d'erreur.<br>

if __name__ == '__main__':
    # Load model
    with open('model.pickle', 'rb') as f:
        model_reg_log = pickle.load(f)
    # launch server in debug mode
    app.run(debug=True)