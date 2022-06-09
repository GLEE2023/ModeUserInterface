from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
	sites = ['Temperature', 'Accelerometer', 'Thermopile', 'Magnetometer', 'Capacitor']
	return render_template("about.html", sites=sites)

@app.route("/home")
def home():
	return render_template("home.html")


@app.route("/everything", methods=['GET','POST'])
def everything():
	if(request.method == 'GET'):
		return render_template("everything.html")
	elif(request.method == 'POST'):
		convCycle = request.form['convCycle'].split(',')
		activeConversionTime = float(convCycle[1])*0.0155
		standbyTime = float(convCycle[0]) - activeConversionTime
		amps = ((135*activeConversionTime) + (1.25*standbyTime))/float(convCycle[0])

		#gyro = request.form['gyro']
		#bypass = request.form['Bypass']
		#fifo = request.form['FIFO']
		return render_template("everything.html", power=request.form)#, inputs = [gyro, bypass, fifo])

@app.route("/power", methods=['POST'])#this is where I think we should call after input from the form.
#we can return a page that gives power and data information. graph? explanation? tradeoffs?
def power():
    power = 0.0#keeping track of the power and data usage.
    data = 0.0
    formData = request.form
    mode = formData['modes']
    match mode:
        case "CC":
            convCycle = request.form['convCycle'].split(',')
    		activeConversionTime = float(convCycle[1])*0.0155#calculation for power of continuous conversion mode TMP117
    		standbyTime = float(convCycle[0]) - activeConversionTime
    		amps = ((135*activeConversionTime) + (1.25*standbyTime))/float(convCycle[0])#unit is microampere, µA
            power += amps
        case "SD":
            power += 1.25 #using the same amps as the standby current. dont think it will make too much of a difference.
        case "OS":
            #addition form is required for one shot i think.
        case ""
    app.run(host='localhost', port=5000)
