from wmata_api import app
import json
import unittest

class WMATATest(unittest.TestCase):
    # ensure both endpoints return a 200 HTTP code
    def test_http_success(self):
        client = app.test_client()

        escalator_response = client.get('/incidents/escalators')
        # assert that the response code of 'incidents/escalators returns a 200 code
        self.assertEqual(escalator_response.status_code, 200)

        elevator_response = client.get('/incidents/elevators')
        # assert that the response code of 'incidents/elevators returns a 200 code
        self.assertEqual(elevator_response.status_code, 200)

################################################################################

    # ensure all returned incidents have the 4 required fields
    def test_required_fields(self):
        required_fields = ["StationCode", "StationName", "UnitType", "UnitName"]

        client = app.test_client()
        response = client.get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        # for each incident in the JSON response assert that each of the required fields
        # are present in the response
        index = 0
        while index < len(json_response):
            item = json_response[index]
            field_index = 0
            while field_index < len(required_fields):
                field = required_fields[field_index]
                self.assertIn(field, item)
                field_index = field_index + 1
            index = index + 1

################################################################################

    # ensure all entries returned by the /escalators endpoint have a UnitType of "ESCALATOR"
    def test_escalators(self):
        client = app.test_client()
        response = client.get('/incidents/escalators')
        json_response = json.loads(response.data.decode())

        # for each incident in the JSON response, assert that the 'UnitType' is "ESCALATOR"
        index = 0
        while index < len(json_response):
            self.assertEqual(json_response[index]["UnitType"], "ESCALATOR")
            index = index + 1

################################################################################

    # ensure all entries returned by the /elevators endpoint have a UnitType of "ELEVATOR"
    def test_elevators(self):
        client = app.test_client()
        response = client.get('/incidents/elevators')
        json_response = json.loads(response.data.decode())

        # for each incident in the JSON response, assert that the 'UnitType' is "ELEVATOR"
        index = 0
        while index < len(json_response):
            self.assertEqual(json_response[index]["UnitType"], "ELEVATOR")
            index = index + 1

################################################################################

if __name__ == "__main__":
    unittest.main()