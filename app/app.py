import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from db_functions import update_or_create_user, get_db
import logging
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

connect_args = {'ssl': {'fake_flag_to_enable_tls': True}}
connection_string = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'

app = Flask(__name__)

app.secret_key = os.urandom(12)
oauth = OAuth(app)
get_db()

@app.route('/')
def index():
    try:
        logging.debug("Successfully reached homepage")
        return render_template('home.html')
    except Exception as e:
        logging.error(f"An error has occurred accessing the home page: {e}")
        return "Exit app and try again"

@app.route('/google/')
def google():
    try:
        logging.debug("Successfully generated Google session")
        CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
        oauth.register(
            name='google',
            client_id=GOOGLE_CLIENT_ID,
            client_secret=GOOGLE_CLIENT_SECRET,
            server_metadata_url=CONF_URL,
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
        redirect_uri = 'https://5000-cs-719093013193-default.cs-us-east1-pkhd.cloudshell.dev/google/auth/'
        return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])
    except Exception as e:
        logging.error(f"An error has occurred generating a Google session: {e}")
        return "Exit app and try again"

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    update_or_create_user(user)
    return redirect('/patients')

@app.route('/patients')
def patients():
    try:
        logging.debug("Successfully redirected to patient directory")
        user = session.get('user')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        patient_id = request.args.get('patient_id')
        blood_sugar_level = request.args.get('blood_sugar_level')
        last_checkup_date = request.args.get('last_checkup_date')
        if user:
            with engine.connect() as connection:
                if first_name:
                    query_1 = text('SELECT * FROM diabetic_patient_info WHERE first_name = :first_name')
                    result_1 = connection.execute(query_1, {"first_name": first_name})
                elif last_name:
                    query_1 = text('SELECT * FROM diabetic_patient_info WHERE last_name = :last_name')
                    result_1 = connection.execute(query_1, {"last_name": last_name})
                elif patient_id:
                    query_1 = text('SELECT * FROM diabetic_patient_info WHERE patient_id = :patient_id')
                    result_1 = connection.execute(query_1, {"patient_id": patient_id})
                elif blood_sugar_level:
                    query_1 = text('SELECT * FROM diabetic_patient_info WHERE blood_sugar_level = :blood_sugar_level')
                    result_1 = connection.execute(query_1, {"blood_sugar_level": blood_sugar_level})
                elif last_checkup_date:
                    query_1 = text('SELECT * FROM diabetic_patient_info WHERE last_checkup_date = :last_checkup_date')
                    result_1 = connection.execute(query_1, {"last_checkup_date": last_checkup_date})
                else:
                    query_1 = text('SELECT * FROM diabetic_patient_info')
                    result_1 = connection.execute(query_1)
                table_data = result_1.fetchall()
            return render_template('patients.html', data=table_data, user=user)
    except Exception as e:
        logging.error(f"Failed to redirect to the patient directory: {e}")
        return "Failed to redirect. Contact site administrator if your account is external to the site network."

@app.route('/info')
def info():
    try:
        logging.debug("Successfully reached user info page")
        user = session.get('user')
        return render_template('dash.html', user=user)
    except Exception as e:
        logging.error(f"Failed to reach user info endpoint: {e}")
        return "Failed to reach user info endpoint. Please restart and try again."

@app.route('/logout')
def logout():
    try:
        logging.debug("Successfully logged out")
        session.pop('user', None)
        return redirect('/')
    except Exception as e:
        logging.error(f"Unable to logout: {e}")
        return "Failed to logout. Please close the app."

if __name__ == '__main__':
    app.run(debug=False, port=8080, host='0.0.0.0')
