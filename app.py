from flask import Flask, jsonify
import feedparser
from datetime import datetime

app = Flask(__name__)

@app.route('/api/entreprises')
def get_entreprises():
    rss_url = "https://www.ejustice.just.fgov.be/cgi_tsv/tsv_rss.pl"
    feed = feedparser.parse(rss_url)

    resultats = []
    for entry in feed.entries:
        if "constitution" in entry.title.lower() and "bruxelles" in entry.title.lower():
            resultats.append({
                "titre": entry.title,
                "lien": entry.link,
                "date": entry.published
            })

    return jsonify(resultats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
