import json
import requests
from flask import Flask, Response

# API endpoint URL's and access keys
WMATA_API_KEY = "799163024d85417fa7703a16a1b22ca4"
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
  if unit_type == "elevators":
    api_unit = "ELEVATOR"
  elif unit_type == "escalators":
    api_unit = "ESCALATOR"
  else:
    return Response(json.dumps({"error": "Invalid unit_type"}), status=400, mimetype="application/json")
  
  # create an empty list called 'incidents'
  incidents = []

  # use 'requests' to do a GET request to the WMATA Incidents API
  response = requests.get(INCIDENTS_URL, headers=headers)
  
  # retrieve the JSON from the response
  data = response.json()
  incident_list = data["ElevatorIncidents"]
  
  
  # iterate through the JSON response and retrieve all incidents matching 'unit_type'
  # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
  #   -StationCode, StationName, UnitType, UnitName
  index = 0
  while index < len(incident_list):
      item = incident_list[index]
      if "UnitType" in item and item["UnitType"] == api_unit:
        incident = {
          "StationCode": item["StationCode"],
          "StationName": item["StationName"],
          "UnitType": item["UnitType"],
          "UnitName": item["UnitName"]
        }
        incidents.append(incident)
      index = index + 1
        

  # return the list of incident dictionaries using json.dumps()
  return Response(json.dumps(incidents, indent=2), mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True)
