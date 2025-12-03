from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)  #comm                                                                                                       
@app.route("/contact/")
def MaPremiereAPI():
     return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

@app.route("/commits/")
def commits_chart():
    # Appel à l'API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)

    if response.status_code != 200:
        return "Erreur lors de l'appel à l'API GitHub"

    commits = response.json()

    # Dictionnaire minute → nombre de commits
    commits_by_minute = {}

    for commit in commits:
        try:
            date_str = commit["commit"]["author"]["date"]   # ex "2024-02-11T11:57:27Z"
            date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute

            commits_by_minute[minute] = commits_by_minute.get(minute, 0) + 1
        except:
            continue

    # On transforme dict en liste pour le HTML
    commits_list = [
        {"minute": minute, "count": count}
        for minute, count in commits_by_minute.items()
    ]

    return render_template("commits.html", commits=commits_list)
  
if __name__ == "__main__":
  app.run(debug=True)
