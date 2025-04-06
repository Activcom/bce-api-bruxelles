from flask import Flask, jsonify, request
import feedparser
import os
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/api/entreprises')
def get_entreprises():
    periode = request.args.get("periode", "jour")  # "jour", "semaine", "mois"
    
    rss_url = "https://www.ejustice.just.fgov.be/cgi_tsv/tsv_rss.pl"
    feed = feedparser.parse(rss_url)

    maintenant = datetime.now()
    
    if periode == "jour":
        date_limite = maintenant - timedelta(days=1)
    elif periode == "semaine":
        date_limite = maintenant - timedelta(days=7)
    elif periode == "mois":
        date_limite = maintenant - timedelta(days=30)
    else:
        date_limite = maintenant - timedelta(days=1)  # par défaut : 1 jour

    resultats = []
    for entry in feed.entries:
        try:
            date_pub = datetime(*entry.published_parsed[:6])
            if date_pub >= date_limite and "constitution" in entry.title.lower():
                resultats.append({
                    "titre": entry.title,
                    "lien": entry.link,
                    "date": entry.published
                })
        except:
            continue

    return jsonify(resultats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
