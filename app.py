import math
from flask import Flask, jsonify, render_template
import yfinance as yf

app = Flask(__name__)

TICKERS = [
    "ANZ.AX", "BHP.AX", "CBA.AX", "WBC.AX", "NAB.AX",
    "MQG.AX", "WES.AX", "CSL.AX", "TLS.AX", "GMG.AX",
    "RIO.AX", "WOW.AX", "TCL.AX", "FMG.AX", "REA.AX",
    "STO.AX", "COL.AX", "IAG.AX", "ALL.AX", "QBE.AX",
    "ASX.AX", "SUN.AX", "SCG.AX", "XRO.AX", "MPL.AX",
    "RMD.AX", "SHL.AX", "APA.AX", "AMC.AX", "TLC.AX",
    "MIN.AX", "JHX.AX", "CPU.AX", "BXB.AX", "ORG.AX",
    "AGL.AX", "NST.AX", "EVN.AX", "TWE.AX", "WTC.AX",
    "NXT.AX", "CWY.AX", "SOL.AX", "PPT.AX", "CAR.AX",
    "ALX.AX", "DOW.AX", "IFL.AX", "360.AX", "PME.AX",
]

COMPANY_NAMES = {
    "ANZ.AX": "ANZ Group",
    "BHP.AX": "BHP Group",
    "CBA.AX": "Commonwealth Bank",
    "WBC.AX": "Westpac Banking",
    "NAB.AX": "National Australia Bank",
    "MQG.AX": "Macquarie Group",
    "WES.AX": "Wesfarmers",
    "CSL.AX": "CSL Limited",
    "TLS.AX": "Telstra Group",
    "GMG.AX": "Goodman Group",
    "RIO.AX": "Rio Tinto",
    "WOW.AX": "Woolworths Group",
    "TCL.AX": "Transurban Group",
    "FMG.AX": "Fortescue",
    "REA.AX": "REA Group",
    "STO.AX": "Santos",
    "COL.AX": "Coles Group",
    "IAG.AX": "Insurance Australia Group",
    "ALL.AX": "Aristocrat Leisure",
    "QBE.AX": "QBE Insurance",
    "ASX.AX": "ASX Limited",
    "SUN.AX": "Suncorp Group",
    "SCG.AX": "Scentre Group",
    "XRO.AX": "Xero",
    "MPL.AX": "Medibank Private",
    "RMD.AX": "ResMed",
    "SHL.AX": "Sonic Healthcare",
    "APA.AX": "APA Group",
    "AMC.AX": "Amcor",
    "TLC.AX": "The Lottery Corporation",
    "MIN.AX": "Mineral Resources",
    "JHX.AX": "James Hardie Industries",
    "CPU.AX": "Computershare",
    "BXB.AX": "Brambles",
    "ORG.AX": "Origin Energy",
    "AGL.AX": "AGL Energy",
    "NST.AX": "Northern Star Resources",
    "EVN.AX": "Evolution Mining",
    "TWE.AX": "Treasury Wine Estates",
    "WTC.AX": "WiseTech Global",
    "NXT.AX": "NextDC",
    "CWY.AX": "Cleanaway Waste Management",
    "SOL.AX": "Washington H. Soul Pattinson",
    "PPT.AX": "Perpetual",
    "CAR.AX": "CAR Group",
    "ALX.AX": "Atlas Arteria",
    "DOW.AX": "Downer EDI",
    "IFL.AX": "Insignia Financial",
    "360.AX": "Life360",
    "PME.AX": "Pro Medicus",
}


def safe_price(val):
    try:
        if val is None or math.isnan(float(val)):
            return None
        return round(float(val), 3)
    except (TypeError, ValueError):
        return None


@app.route("/")
def index():
    return render_template("index.html")


def _fetch_close(tickers, **kwargs):
    data = yf.download(tickers, auto_adjust=True, progress=False, threads=True, **kwargs)
    last_row = data["Close"].iloc[-1]
    result = {}
    for ticker in tickers:
        result[ticker] = safe_price(last_row[ticker]) if ticker in last_row.index else None
    return result


@app.route("/api/prices")
def prices():
    """Returns both historical and current prices fetched in parallel."""
    try:
        historical = _fetch_close(TICKERS, start="2026-02-25", end="2026-03-01")
        current = _fetch_close(TICKERS, period="5d", interval="1d")
        return jsonify({"historical": historical, "current": current})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/current")
def current():
    try:
        result = _fetch_close(TICKERS, period="5d", interval="1d")
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
