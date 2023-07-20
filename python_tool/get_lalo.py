import json

# Read JSON fragment from txt file
with open("output.txt", "r") as file:
    json_data = json.load(file)

# Extract all "aircraftLocation" and "altitude" data
location_altitude_data = []
for frame_state in json_data["info"]["frameTimeStates"]:
    aircraft_location = frame_state["flightControllerState"]["aircraftLocation"]
    altitude = frame_state["flightControllerState"]["altitude"]
    location_altitude_data.append({"latitude": aircraft_location["latitude"], "longitude": aircraft_location["longitude"], "altitude": altitude})

# Write values to a new txt file
with open("lalo_output.txt", "w") as f:
    for data in location_altitude_data:
        f.write(f"latitude: {data['latitude']}, longitude: {data['longitude']}, altitude: {data['altitude']}\n")

print("Values extracted and written to 'output.txt' file.")
