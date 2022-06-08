from flask import Flask, render_template, request

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
	
@app.route("/home")
def home():
	return render_template("home.html")

app.run(host='localhost', port=5000)
@app.route("/everything", methods=['GET','POST'])
def everything():
    if(request.method == 'GET'):
        return render_template("everything.html")
    elif(request.method == 'POST'):
        convCycle = request.form['convCycle'].split(',')
        activeConversionTime = float(convCycle[1])*0.0155
        standbyTime = float(convCycle[0]) - activeConversionTime
        amps = ((135*activeConversionTime) + (1.25*standbyTime))/float(convCycle[0])


        return render_template("everything.html", power=amps*3.3)
