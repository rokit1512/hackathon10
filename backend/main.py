from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/uploadentry', methods=["POST"])
def upload_daily_entry():
    try:
        userID = request.form["userID"]
        moods = request.form["moods"]
        stress = request.form["stress"]
        journalEntry = request.form["journalEntry"]
        journalSentiment = analysis.sentiment_score(journalEntry) # -1 to 1
        #journalSentiment + 1 is 0 to 2
        # times 50 is 0 to 100
        #then round to int
        moodInt = round((50*(journalSentiment+1)))
    except:
        return 

if __name__ == "__main__":
    app.run(port=5000, debug=True)
