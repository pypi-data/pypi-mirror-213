import requests
import time
import re
import socket

class ioc():
    def __init__(self, api_token = "", limit = 10):
        self.api_token = api_token
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.limit = limit
        self.json_data = {
            'api_token': self.api_token,
            'limit': self.limit,
        }

    def daily_ioc(self,):
        if self.api_token == "":
            return print("Please Use Your API Token")
        if self.limit > 100:
            return print("Limit can not exceed 100")

        return requests.post(
            'https://ioc.threatmonit.io/api/daily-ioc/',
            headers=self.headers,
            json=self.json_data,
        ).json()

    def QRadarIntegrator(self, 
                        import_data,
                        qradar_auth_key,
                        qradar_server,
                        qradar_ref_set
                        ):
        
        # self.qradar_auth_key = "811aacf9-jh68-444h-98f4-5d25b7a94844"
        self.qradar_ref_set = "THREATMON_Event_IOC"

        QRadar_POST_url = f"https://{qradar_server}/api/reference_data/sets/bulk_load/{qradar_ref_set}"

        self.QRadar_headers = {
            'sec': qradar_auth_key,
            'content-type': "application/json",
        }

        print(time.strftime("%H:%M:%S") + " -- " + "Initiating, IOC POST to QRadar ")
        files = []

        for key in import_data["entities"]:
            files.extend(ioc["hash"] for ioc in key["hashes"])
            
        qradar_response = requests.request("POST", QRadar_POST_url, data=files, headers=self.QRadar_headers, verify=False)
        if qradar_response.status_code == 200:
            print(time.strftime("%H:%M:%S") + " -- " + " (Finished) Imported IOCs to QRadar (Success)" )
        else:
            print(time.strftime("%H:%M:%S") + " -- " + "Could not POST IOCs to QRadar (Failure)")