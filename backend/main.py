from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from flask import url_for
from flask import render_template
from flask_cors import CORS
import psycopg2

import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

import analysis

app = Flask(__name__)
CORS(app)

load_dotenv()
#from supabase example code
# Fetch variables
USER = os.getenv("dbuser")
PASSWORD = os.getenv("dbpassword")
HOST = os.getenv("dbhost")
PORT = os.getenv("dbport")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")

@app.route('/api/uploadentry', methods=["POST"])
def upload_daily_entry():
    try:
        content = request.json
        userID = content["userID"]
        moods = content["moods"]
        stress = content["stress"]
        journalEntry = content["journalEntry"]
        journalSentiment = analysis.sentiment_score(journalEntry) # -1 to 1
        #journalSentiment + 1 is 0 to 2
        # times 50 is 0 to 100
        #then round to int
        moodInt = round((50*(journalSentiment+1)))
        date = datetime.today().strftime("%d/%m/%Y")
        connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
        )
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        ##moods , mood_int, journal_entry, stress
        cursor.execute('''INSERT INTO "moodDashboard" VALUES (%s, %s, %s, %s, %s, %s)''', (json.dumps(moods), moodInt, json.dumps(journalEntry), stress, date, userID))
        connection.commit()
        cursor.close()
        connection.close()
        return "200 OK", 200
    except Exception as e:
        return f"{e}", 500

@app.route("/journal", methods=["GET"])
def serve_html():
    return render_template("../FrontEnd.html")

@app.route("/api/dailyquote", methods=["GET"])
def get_daily_quote():
    try:
        date = datetime.today().strftime("%d/%m/%Y")
        randomState = random.Random()
        randomState.seed(date)
        with open("./static/quotes.txt") as quoteFile:
            quotes = quoteFile.readlines()
            currentQuote = randomState.choice(quotes)
            return {"quote": currentQuote}, 200
    except Exception as e:
        return f"{e}", 500

@app.route("/api/streakimage", methods=["GET"])
def get_streak_image(): # get url/api/streakimage?streak=number
    try:
        streakStr = request.args.get("streak")
        streak = int(streakStr)

    except Exception as e:
        print(e)
        return "Error", 500
    
@app.route("/api/streakfromid", methods=["GET"])
def get_streak_from_id():
    try:
        id = request.args.get("id")
        connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
        )
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        ##moods , mood_int, journal_entry, stress
        cursor.execute('''SELECT date FROM "moodDashboard" WHERE user_id = %s''', id)
        dates = set(cursor.fetchall())
        day = datetime.today()
        dayDelta = timedelta(days=1)
        streak = 0
        while (day.strftime("%d/%m/%Y"),) in dates:
            streak += 1
            day = day - dayDelta
        cursor.close()
        connection.close()
        if streak == 0:
            return {"streak": streak, "streakimage": url_for('static', filename='streak-bad.jpg')}
        elif streak <=10:
            return send_file("./static/streak-okay.jpg", mimetype="image/jpeg")
        elif streak > 10:
            return send_file("./static/streak-good.jpg", mimetype="image/jpeg")
        else:
            print("Error")
            return "Error", 500
        toReturn = {"streak": streak, "streakimage": str(url_for("get_streak_image"))+"?streak="+str(streak)}
    except Exception as e:
        print(e)
        return "Error", 500

@app.route("/api/getinfo")
def get_table_from_id():
    pass

if __name__ == "__main__":
    app.run(port=5000, debug=True)
