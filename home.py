from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
	sites = ['Temperature', 'Accelerometer', 'Thermopile', 'Magnetometer', 'Capacitor']
	return render_template("about.html", sites=sites)
 
@app.route("/accelerometer")
def accelerometer():
	return render_template("accelerometer.html")
 
@app.route("/magnetometer")
def magnetometer():
	return render_template("magnetometer.html")

@app.route("/TMP117")
def TMP117():
	return render_template("TMP117.html")
app.run(host='localhost', port=5000)
