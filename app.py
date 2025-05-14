from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Function to get relay status from the database
def get_relay_status():
    conn = sqlite3.connect("relay.db")
    cur = conn.execute("SELECT relay_state FROM relay_status WHERE relay_id=1")
    row = cur.fetchone()
    print(row)
    conn.close()
    #return row[1] if row else "OFF"
    print(row[0])
    if row[0] == "ON":
        return "01"
    else:
        return "00"

# Route to render the main page with relay status
@app.route("/")
def home():
    relay_status = get_relay_status()
    return render_template("index.html", relay_status=relay_status)

# Route to control relay ON/OFF
@app.route("/relay/<status>")
def control_relay(status):
    if status not in ["ON", "OFF"]:
        return "Invalid command! Use ON or OFF."

    conn = sqlite3.connect("relay.db")
    cur = conn.execute("SELECT * FROM relay_status WHERE relay_id=1")
    row = cur.fetchone()

    if row is None:
        conn.execute("INSERT INTO relay_status (relay_id, relay_state) VALUES (1, ?)", (status,))
    else:
        conn.execute("UPDATE relay_status SET relay_state=? WHERE relay_id=1", (status,))

    conn.commit()
    conn.close()

    return render_template("index.html", relay_status=status)

# Route to check current relay status
@app.route("/check_relay")
def check_relay():
    relay_status = get_relay_status()
    return relay_status

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
