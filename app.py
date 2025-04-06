from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

def get_bce_data(start_date):
    url = "https://kbopub.economie.fgov.be/kbo_web_service/public/search/criteria"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "searchTerm": "",
        "language": "FR",
        "startDate": start_date.strftime('%Y-%m-%d'),
        "entityStatus": "ACTIVE"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []

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

    entreprises = get_bce_data(date_debut)

    resultats = []
    for ent in entreprises:
        resultats.append({
            "nom": ent.get("denomination"),
            "numero_bce": ent.get("enterpriseNumber"),
            "forme": ent.get("legalForm"),
            "date": ent.get("startDate"),
            "adresse": ent.get("addresses")[0]["street"] if ent.get("addresses") else "",
        })

    return jsonify(resultats)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
