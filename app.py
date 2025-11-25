# from flask import Flask, request
# from simulator.simulator import GPSSimulator

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return '''
#         <h2>GPS Simulator Web App</h2>
#         <form action="/simulate" method="post">
#             Device ID: <input type="text" name="device_id" required><br><br>
#             Start Latitude: <input type="text" name="start_lat" required><br>
#             Start Longitude: <input type="text" name="start_lon" required><br>
#             End Latitude: <input type="text" name="end_lat" required><br>
#             End Longitude: <input type="text" name="end_lon" required><br>
#             Frequency (seconds): <input type="number" name="frequency" value="2"><br><br>
#             <input type="submit" value="Start Simulation">
#         </form>
#     '''

# @app.route('/simulate', methods=['POST'])
# def simulate():
#     device_id = request.form['device_id']
#     start_lat = float(request.form['start_lat'])
#     start_lon = float(request.form['start_lon'])
#     end_lat = float(request.form['end_lat'])
#     end_lon = float(request.form['end_lon'])
#     frequency = int(request.form.get('frequency', 2))
#     server_url = "http://telematics.kofleetz.com:5055"

#     waypoints = [(start_lat, start_lon), (end_lat, end_lon)]
#     simulator = GPSSimulator(server_url, device_id, waypoints, frequency)
#     simulator.run()
#     return "Simulation started!"

# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, request, redirect
import threading

from simulator.simulator import GPSSimulator

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>GPS Simulator Web App</title>
            <style>
                body {
                    background: #e6f0ff;
                    font-family: Arial, sans-serif;
                }
                .form-container {
                    max-width: 400px;
                    margin: 60px auto;
                    background: #fff;
                    box-shadow: 0 2px 12px #bbb;
                    border-radius: 12px;
                    padding: 30px 40px;
                }
                h2 {
                    text-align: center;
                    margin-bottom: 25px;
                }
                label {
                    display: block;
                    margin-bottom: 6px;
                    font-weight: bold;
                }
                input[type="text"], input[type="number"] {
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 16px;
                    border-radius: 4px;
                    border: 1px solid #aaa;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    width: 100%;
                    padding: 10px;
                    background-color: #3399FF;
                    color: #fff;
                    font-size: 16px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #2676cc;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h2>GPS Simulator Web App</h2>
                <form action="/simulate" method="post">
                    <label for="device_id">Device ID</label>
                    <input type="text" id="device_id" name="device_id" required>

                    <label for="start_lat">Start Latitude</label>
                    <input type="text" id="start_lat" name="start_lat" required pattern="^-?\\d+(\\.\\d+)?$">

                    <label for="start_lon">Start Longitude</label>
                    <input type="text" id="start_lon" name="start_lon" required pattern="^-?\\d+(\\.\\d+)?$">

                    <label for="end_lat">End Latitude</label>
                    <input type="text" id="end_lat" name="end_lat" required pattern="^-?\\d+(\\.\\d+)?$">

                    <label for="end_lon">End Longitude</label>
                    <input type="text" id="end_lon" name="end_lon" required pattern="^-?\\d+(\\.\\d+)?$">

                    <label for="frequency">Frequency (seconds)</label>
                    <input type="number" id="frequency" name="frequency" value="2" min="1" required>

                    <input type="submit" value="Start Simulation">
                </form>
            </div>
        </body>
        </html>
    '''

def run_simulation_in_background(simulator):
    simulator.run()

@app.route('/simulate', methods=['POST'])
def simulate():
    device_id = request.form['device_id']
    start_lat = float(request.form['start_lat'])
    start_lon = float(request.form['start_lon'])
    end_lat = float(request.form['end_lat'])
    end_lon = float(request.form['end_lon'])
    frequency = int(request.form.get('frequency', 2))
    server_url = "http://telematics.kofleetz.com:5055"

    waypoints = [(start_lat, start_lon), (end_lat, end_lon)]
    simulator = GPSSimulator(server_url, device_id, waypoints, frequency)
    # Run the simulator in the background to avoid delaying the redirect
    threading.Thread(target=run_simulation_in_background, args=(simulator,), daemon=True).start()
    return redirect("https://telematics.kofleetz.com/")

if __name__ == "__main__":
    app.run(debug=True)
