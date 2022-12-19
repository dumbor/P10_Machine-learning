from asyncio.log import logger
from distutils.log import error
from flask import Flask, make_response, request, render_template, flash, abort, redirect, url_for
import io
from io import StringIO
import pandas as pd
import numpy as np
import pickle
import ast


app = Flask(__name__)

# Secret key requested to avoid error message
app.secret_key="blablabla"



# DEFAULT ROUTE
@app.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")


# PREDICTION ROUTE
@app.route('/predict', methods=["POST"])
def predict_view():
    try:
        #flash("Résultat de la prédiction")
        f = request.files['file_name'] # file name from html
        if not f:
            return "No file"
        
        # Preparing file reading
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        stream.seek(0) # we focus on the begining of the file (0). Without this code row, there's an error.
        result = stream.read()

        # convert my file to dataframe
        df = pd.read_csv(StringIO(result))
        
        # load my prediction model from disk and predict
        model = pickle.load(open('model.pickle', 'rb')) 
        df['prediction'] = model.predict(df.iloc[:,0:6])
        df['prediction'] = np.where(df['prediction']==0,"False", "True")

        # Calculation of probabilities for each line to be true or false
        y_proba=pd.DataFrame(model.predict_proba(df.iloc[:,0:6]), columns=["%_prob_false","%_prob_true"])
        y_proba=np.round(y_proba*100,2)

        # Concatenate df and proba in one dataframe
        prod_banknotes=pd.concat([df,y_proba], axis=1)

        return render_template("predict.html", column_names=prod_banknotes.columns.values.tolist(), row_data=(prod_banknotes.values.tolist()), zip=zip)
    
    except Exception as e:
        msg_error=f"L'erreur suivante s'est produite : {e}. Vérifiez votre fichier et recommencez."
        return render_template('index.html', error=msg_error)


# SAVING FILE ROUTE
@app.route('/save', methods=["POST"])
def save_view():
    # I retrieve data from my hidden fields in the form.
    # Data are String at this point
    get_data=request.form['my_data']
    get_col=request.form['my_columns']

    # Converting data in String format to List to be exported in csv file
    data_list = ast.literal_eval(get_data)
    col_list = ast.literal_eval(get_col)

    # Create the dataframe to be exported
    prod_banknotes=pd.DataFrame(data_list, columns=[col_list],)

    response = make_response(prod_banknotes.to_csv(index=False))
    response.headers["Content-Disposition"] = "attachment; filename=prediction_api_result.csv"
    return response

# Start server with debug mode (only on dev environment)
if __name__ == '__main__':
    app.run(port = 9000, debug=True)
