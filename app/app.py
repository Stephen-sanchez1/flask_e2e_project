from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://<stephen-db>:<Happy123>@<db_host>/<db_name>'
db = SQLAlchemy(app)

class BloodSugarReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

@app.route('/')
def home():
    readings = BloodSugarReading.query.all()
    return render_template('home.html', readings=readings)

@app.route('/add_reading', methods=['POST'])
def add_reading():
    value = request.form['value']
    # You can add validation and processing here
    new_reading = BloodSugarReading(value=value)
    db.session.add(new_reading)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
