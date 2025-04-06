from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# Google Sheets hitelesítés (modern mód)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file(
    'service_account.json',
    scopes=SCOPES
)

client = gspread.authorize(creds)
sheet = client.open("KoltsegKoveto").sheet1  # Sheet neve

@app.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    tetel = data.get('tetel')
    osszeg = data.get('osszeg')
    megjegyzes = data.get('megjegyzes', '')

    if not tetel or not osszeg:
        return jsonify({"error": "Hiányzó adat"}), 400

    datum = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([datum, tetel, osszeg, megjegyzes])
    
    return jsonify({"message": "Sikeresen rögzítve!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
