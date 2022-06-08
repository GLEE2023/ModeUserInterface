from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
	sites = ['Temperature', 'Accelerometer', 'Thermopile', 'Magnetometer', 'Capacitor']
	return render_template("about.html", sites=sites)

@app.route("/tmp117", methods=['GET','POST'])
def tmp117():
    if(request.method == 'GET'):
        return render_template("TMP117.html")
    elif(request.method == 'POST'):
        convCycle = request.form['convCycle'].split(',')
        activeConversionTime = float(convCycle[1])*0.0155
        standbyTime = float(convCycle[0]) - activeConversionTime
        amps = ((135*activeConversionTime) + (1.25*standbyTime))/float(convCycle[0])

        return render_template("TMP117.html", power=amps*3.3)
