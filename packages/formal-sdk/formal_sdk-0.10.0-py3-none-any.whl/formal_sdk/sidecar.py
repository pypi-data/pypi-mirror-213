import json

import requests


class SidecarService:

    def __init__(self, SERVER_URL, token):
        self.BASE_URL = SERVER_URL
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': token,
        }

    def GetTLSCertificate(self, sidecarId):

        url = f"{self.BASE_URL}/admin/sidecars/{sidecarId}/tlscert"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        secret = json.loads(response.json().get('secret', {}))

        if 'certificate' not in secret or 'private_key' not in secret:
            raise Exception('Invalid response')

        return secret['certificate'], secret['private_key'], str(secret)
