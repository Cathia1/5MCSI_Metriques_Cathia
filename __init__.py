from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen, Request
from collections import Counter
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
def commits():
    # 1. Appel de l’API GitHub
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)

    if response.status_code != 200:
        return "Erreur API GitHub", 500

    commits_json = response.json()
  
    # 2. Extraction des minutes
    minutes = []
    for c in commits_json:
        try:
            date_str = c["commit"]["author"]["date"]  # ex: "2024-02-11T11:57:27Z"
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minutes.append(date_obj.minute)
        except:
            pass  # ignore les erreurs

    # 3. Comptage des commits par minute
    count_by_minute = Counter(minutes)

    # 4. Préparation à envoyer au HTML
    commits_list = []
    for minute, count in count_by_minute.items():
        commits_list.append({"minute": minute, "count": count})

    # TRI pour éviter les erreurs d'affichage
    commits_list = sorted(commits_list, key=lambda x: x["minute"])

    # 5. Envoi au template
    return render_template("commits.html", commits=commits_list)
  
if __name__ == "__main__":
  app.run(debug=True)
