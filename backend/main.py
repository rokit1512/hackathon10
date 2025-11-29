from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/uploadentry', methods=["POST"])
def upload_daily_entry():
    moods = request.form["moods"]
    stress = request.form["stress"]
    journalEntry = request.form["journalEntry"]


if __name__ == "__main__":
    app.run(port=5000, debug=True)
