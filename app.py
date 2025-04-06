from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

def scrape_bce(date_debut):
    url = "https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html"

    # Format de la date attendu par le site
    date_str = date_debut.strftime('%d/%m/%Y')

    params = {
        "lang": "fr",
        "hoofdstatus": "ACT",
        "startdatumvan": date_str,
        "actie": "Zoeken"
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'resultTable'})
    resultats = []

    if not table:
        return []

    rows = table.find_all('tr')[1:]  # skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:
            nom = cols[0].text.strip()
            numero_bce = cols[1].text.strip()
            forme = cols[2].text.strip()
            resultats.append({
                "nom": nom,
                "numero_bce": numero_bce,
                "forme": forme
            })

    return resultats

@app.route('/api/entreprises')
def entreprises():
    periode = request.args.get("periode", "jour")
    now = datetime.now()

    if periode == "jour":
        date_debut = now - timedelta(days=1)
    elif periode == "semaine":
        date_debut = now - timedelta(days=7)
    elif periode == "mois":
        date_debut = now - timedelta(days=30)
    else:
        date_debut = now - timedelta(days=1)

    data = scrape_bce(date_debut)
    return jsonify(data)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
