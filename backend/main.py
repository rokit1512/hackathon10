from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS
import os
import psycopg2
import json
from datetime import datetime


import analysis

app = Flask(__name__)
CORS(app)

#from supabase example code
# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
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

if __name__ == "__main__":
    app.run(port=5000, debug=True)
