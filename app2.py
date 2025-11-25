# from flask import Flask, request, redirect
# import threading

# from simulator.simulator import GPSSimulator  # Ensure this matches your project

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return '''
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <title>GPS Waypoint Simulator</title>
#             <meta charset="UTF-8">
#             <style>
#                 body { background: #e6f0ff; font-family: Arial, sans-serif; }
#                 .form-container {
#                     max-width: 500px; margin: 60px auto;
#                     background: #fff; box-shadow: 0 2px 12px #bbb;
#                     border-radius: 12px; padding: 30px 40px;
#                 }
#                 h2 { text-align: center; margin-bottom: 25px; }
#                 label { display: block; margin-bottom: 8px; font-weight: bold; }
#                 .waypoint-row {
#                     display: flex; gap: 10px; margin-bottom: 12px;
#                 }
#                 .waypoint-row input { flex: 1; }
#                 #add-waypoint-btn {
#                     margin-bottom: 20px; padding: 8px 14px;
#                     background: #3399FF; color: #fff; border-radius: 4px;
#                     border: none; cursor: pointer;
#                 }
#                 #add-waypoint-btn:hover { background: #2676cc; }
#                 input[type="text"], input[type="number"] {
#                     width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #aaa;
#                     box-sizing: border-box;
#                 }
#                 input[type="submit"] {
#                     width: 100%; padding: 10px; background-color: #3399FF;
#                     color: #fff; font-size: 16px; border: none; border-radius: 5px;
#                     cursor: pointer;
#                 }
#                 input[type="submit"]:hover { background-color: #2676cc; }
#             </style>
#         </head>
#         <body>
#             <div class="form-container">
#                 <h2>GPS Waypoint Simulator</h2>
#                 <form action="/simulate" method="post" id="waypoint-form">
#                     <label for="device_id">Device ID</label>
#                     <input type="text" id="device_id" name="device_id" required>
#                     <div id="waypoints">
#                         <div class="waypoint-row">
#                             <input type="text" name="latitude" placeholder="Latitude" required pattern="^-?\\d+(\\.\\d+)?$">
#                             <input type="text" name="longitude" placeholder="Longitude" required pattern="^-?\\d+(\\.\\d+)?$">
#                         </div>
#                         <div class="waypoint-row">
#                             <input type="text" name="latitude" placeholder="Latitude" required pattern="^-?\\d+(\\.\\d+)?$">
#                             <input type="text" name="longitude" placeholder="Longitude" required pattern="^-?\\d+(\\.\\d+)?$">
#                         </div>
#                     </div>
#                     <button type="button" id="add-waypoint-btn" onclick="addWaypoint()">Add Waypoint</button>
#                     <label for="frequency">Frequency (seconds)</label>
#                     <input type="number" id="frequency" name="frequency" value="2" min="1" required>
#                     <input type="submit" value="Start Simulation">
#                 </form>
#             </div>
#             <script>
#                 function addWaypoint() {
#                     var wp = document.createElement('div');
#                     wp.className = "waypoint-row";
#                     wp.innerHTML =
#                       `<input type="text" name="latitude" placeholder="Latitude" required pattern="^-?\\d+(\\.\\d+)?$">
#                        <input type="text" name="longitude" placeholder="Longitude" required pattern="^-?\\d+(\\.\\d+)?$">`;
#                     document.getElementById('waypoints').appendChild(wp);
#                 }
#             </script>
#         </body>
#         </html>
#     '''

# def run_sim_in_background(simulator):
#     simulator.run()

# @app.route('/simulate', methods=['POST'])
# def simulate():
#     device_id = request.form['device_id']
#     lat_list = request.form.getlist('latitude')
#     lon_list = request.form.getlist('longitude')
#     frequency = int(request.form.get('frequency', 2))
#     server_url = "http://telematics.kofleetz.com:5055"  # Or your Traccar endpoint

#     waypoints = []
#     for lat, lon in zip(lat_list, lon_list):
#         try:
#             waypoints.append((float(lat), float(lon)))
#         except ValueError:
#             continue  # skip any invalid input

#     # Run the simulation in the background and redirect immediately
#     simulator = GPSSimulator(server_url, device_id, waypoints, frequency)
#     threading.Thread(target=run_sim_in_background, args=(simulator,), daemon=True).start()

#     return redirect("https://telematics.kofleetz.com/")

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, redirect
import threading

from simulator.simulator import GPSSimulator  # Ensure this matches your project structure

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>GPS Waypoint Simulator</title>
            <meta charset="UTF-8">
            <style>
                body { background: #e6f0ff; font-family: Arial, sans-serif; }
                .form-container {
                    max-width: 500px; margin: 60px auto;
                    background: #fff; box-shadow: 0 2px 12px #bbb;
                    border-radius: 12px; padding: 30px 40px;
                }
                h2 { text-align: center; margin-bottom: 25px; }
                label { display: block; margin-bottom: 8px; font-weight: bold; }
                .waypoint-row {
                    display: flex; gap: 10px; margin-bottom: 12px;
                }
                .waypoint-row input { flex: 1; }
                #add-waypoint-btn {
                    margin-bottom: 20px; padding: 8px 14px;
                    background: #3399FF; color: #fff; border-radius: 4px;
                    border: none; cursor: pointer;
                }
                #add-waypoint-btn:hover { background: #2676cc; }
                input[type="number"] {
                    width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #aaa;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    width: 100%; padding: 10px; background-color: #3399FF;
                    color: #fff; font-size: 16px; border: none; border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover { background-color: #2676cc; }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h2>GPS Waypoint Simulator</h2>
                <form action="/simulate" method="post" id="waypoint-form">
                    <label for="device_id">Device ID</label>
                    <input type="text" id="device_id" name="device_id" required>
                    <div id="waypoints">
                        <div class="waypoint-row">
                            <input type="number" name="latitude" placeholder="Latitude" required min="-90" max="90" step="any">
                            <input type="number" name="longitude" placeholder="Longitude" required min="-180" max="180" step="any">
                        </div>
                        <div class="waypoint-row">
                            <input type="number" name="latitude" placeholder="Latitude" required min="-90" max="90" step="any">
                            <input type="number" name="longitude" placeholder="Longitude" required min="-180" max="180" step="any">
                        </div>
                    </div>
                    <button type="button" id="add-waypoint-btn" onclick="addWaypoint()">Add Waypoint</button>
                    <label for="frequency">Frequency (seconds)</label>
                    <input type="number" id="frequency" name="frequency" value="2" min="1" required>
                    <input type="submit" value="Start Simulation">
                </form>
            </div>
            <script>
                function addWaypoint() {
                    var wp = document.createElement('div');
                    wp.className = "waypoint-row";
                    wp.innerHTML =
                        `<input type="number" name="latitude" placeholder="Latitude" required min="-90" max="90" step="any">
                         <input type="number" name="longitude" placeholder="Longitude" required min="-180" max="180" step="any">`;
                    document.getElementById('waypoints').appendChild(wp);
                }
            </script>
        </body>
        </html>
    '''

def run_sim_in_background(simulator):
    simulator.run()

@app.route('/simulate', methods=['POST'])
def simulate():
    device_id = request.form['device_id']
    lat_list = request.form.getlist('latitude')
    lon_list = request.form.getlist('longitude')
    frequency = int(request.form.get('frequency', 2))
    server_url = "http://telematics.kofleetz.com:5055"  # Or your Traccar endpoint

    waypoints = []
    for lat, lon in zip(lat_list, lon_list):
        try:
            waypoints.append((float(lat), float(lon)))
        except ValueError:
            continue  # skip any invalid input

    # Run the simulation in the background and redirect immediately
    simulator = GPSSimulator(server_url, device_id, waypoints, frequency)
    threading.Thread(target=run_sim_in_background, args=(simulator,), daemon=True).start()

    return redirect("https://telematics.kofleetz.com/")

if __name__ == "__main__":
    app.run(debug=True)
