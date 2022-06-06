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
 


 
app.run(host='localhost', port=5000)