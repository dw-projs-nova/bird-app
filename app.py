import json
import urllib.error
import urllib.request
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "BirdApp/1.0"})
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.load(response)

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

@app.route('/facts')
def factsPage():
    pages = ["American_robin", "Barn_owl", "Peregrine_falcon"]
    title = pages[datetime.now().timetuple().tm_yday % len(pages)]
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    try:
        summary = fetch_json(url)
        bird = {
            "name": summary.get("title", title.replace("_", " ")),
            "summary": summary.get("extract", "Bird information is unavailable."),
            "image": summary.get("thumbnail", {}).get("source"),
            "url": summary.get("content_urls", {}).get("desktop", {}).get("page"),
        }
    except (urllib.error.URLError, TimeoutError, ValueError):
        bird = {
            "name": title.replace("_", " "),
            "summary": "Bird information is temporarily unavailable.",
            "image": None,
            "url": None,
        }
    return render_template('facts.html', bird=bird)

@app.route('/bird-of-the-day')
def birdOfTheDayPage():
    url = "https://api.inaturalist.org/v1/observations?taxon_id=3&quality_grade=research&photos=true&order=desc&order_by=observed_on&per_page=1"
    try:
        observations = fetch_json(url).get("results", [])
        observation = observations[0] if observations else {}
        taxon = observation.get("taxon") or {}
        photos = observation.get("photos") or []
        photo = photos[0] if photos else {}
        bird = {
            "name": taxon.get("preferred_common_name") or taxon.get("name") or "Bird data unavailable",
            "date": observation.get("observed_on"),
            "url": observation.get("uri"),
            "image": photo.get("url"),
            "attribution": photo.get("attribution"),
        }
    except (urllib.error.URLError, TimeoutError, ValueError):
        bird = {
            "name": "Bird data temporarily unavailable",
            "date": None,
            "url": None,
            "image": None,
            "attribution": None,
        }
    return render_template('bird_of_the_day.html', bird=bird)
