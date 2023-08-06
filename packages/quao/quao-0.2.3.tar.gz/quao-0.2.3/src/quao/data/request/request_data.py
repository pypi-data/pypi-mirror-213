"""
    QuaO Project request_data.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""


class RequestData:

    def __init__(self, event):
        json_data = event.json()
        self.data = json_data
        self.input = json_data.get("input")
        self.shots = json_data.get("shots")
        self.device_id = json_data.get("deviceId")
        self.sdk = json_data.get("sdk").lower() if json_data.get("sdk") else None
        self.server_url = json_data.get("serverUrl")
        self.circuit_export_url = json_data.get("circuitExportUrl")
