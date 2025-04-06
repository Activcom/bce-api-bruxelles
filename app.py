from flask import Flask, jsonify
import feedparser
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/entreprises')
def get_all():
    rss_url = "https://www.ejustice.just.fgov.be/cgi_tsv/tsv_rss.pl"
    feed = feedparser.parse(rss_url)

    resultats = []
    for entry in feed.entries[:30]:  # on limite à 30 résultats pour éviter trop de données
        resultats.append({
            "titre": entry.title,
            "lien": entry.link,
            "date": entry.published
        })

    return jsonify(resultats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
