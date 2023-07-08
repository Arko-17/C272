import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    Twilio_account_sid='ACeeaf03b9b8804b6f7c08593b0e06ebc7'
    Twilio_sync_service_sid='IS4e0ab12d56ca59efdea9e5adc1f038ac'
    twilio_api_key='SKce6fe065681eb273dfcfdc150153b6b6'
    twilio_api_secret='23YNAjULu33JD9kB92jgnlGe6GAmnitV'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(Twilio_account_sid, twilio_api_key, twilio_api_secret, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(Twilio_sync_service_sid)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():

    text_from_textarea=request.form['text']
    with open('collaborative.txt','w') as f:
        f.write(text_from_textarea)
    file_to_store_text="collaborative.txt"
    return send_file(file_to_store_text,as_attachment=True)
    
if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
