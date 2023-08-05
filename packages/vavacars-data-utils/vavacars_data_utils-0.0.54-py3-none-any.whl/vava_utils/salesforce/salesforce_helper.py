import os
import requests
import pandas as pd

MAX_ATTEMPTS = 5


class SalesForceHelper:
    def __init__(
        self,
        client_id,
        client_secret,
        username,
        password,
        url="https://vavacarsturkey.my.salesforce.com/services/data/v57.0",
    ):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://login.salesforce.com/services/oauth2/token"
        payload = f"grant_type=password&client_id={self.client_id}&client_secret={self.client_secret}&username={self.username}&password={self.password}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()["access_token"]

    def query(self, query_str, attempt=1, as_frame=True):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        url = os.path.join(self.url, f"query/?q={query_str}")
        response = requests.request("GET", url, headers=headers)
        try:
            response.raise_for_status()
            if as_frame:
                return pd.DataFrame(response.json()["records"])
            else:
                return response.json()
        except Exception as e:
            if attempt < MAX_ATTEMPTS:
                self.get_access_token()
                return self.query(query_str, attempt + 1)
            else:
                raise e
