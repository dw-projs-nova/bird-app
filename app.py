from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/birds')
def birdPage():
    return render_template('bird.html')

@app.route('/seasons')
def seasonsPage():
    current_date = datetime.now()
    return render_template('seasons.html', month=current_date.strftime("%B"), year=current_date.year)
