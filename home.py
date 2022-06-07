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
        convCycle = eval(request.form['convCycle'].split(', ')[0])#BAD PRACTICE! DONT USE!
        #convCycle is a tuple, (conversion cycle time, averaging)
        activeConversionTime = convCycle[1]*0.0155
        standbyTime = convCycle[0] - activeConversionTime
        amps = ((135*activeConversionTime) + (1.25*standbyTime))/convCycle[0]
        debugArray = [convCycle, activeConversionTime, standbyTime, amps*3.3]

        return render_template("TMP117.html", debugArray=debugArray)
