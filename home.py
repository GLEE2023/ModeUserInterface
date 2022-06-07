from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
	sites = ['Temperature', 'Accelerometer', 'Thermopile', 'Magnetometer', 'Capacitor']
	return render_template("about.html", sites=sites)

@app.route("/tmp117")
def tmp117():
	return render_template("TMP117.html")
