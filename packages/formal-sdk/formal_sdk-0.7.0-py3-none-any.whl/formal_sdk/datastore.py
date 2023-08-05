import requests
import json


class NativeRole:
    def __init__(self, datastoreId, nativeRoleId, nativeRoleSecret, useAsDefault):
        self.dataStoreId = datastoreId
        self.nativeRoleId = nativeRoleId
        self.nativeRoleSecret = nativeRoleSecret
        self.useAsDefault = useAsDefault

    def to_dict(self):
        return self.__dict__


class DataStoreService:

    def __init__(self, SERVER_URL, token):
        self.BASE_URL = SERVER_URL
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': token,
        }

    def CreateNativeRole(self, dataStoreId, nativeRoleId, nativeRoleSecret, useAsDefault):
        url = f"{self.BASE_URL}/admin.v1.DataStoreService/CreateNativeRole"
        payload = {
            'dataStoreId': dataStoreId,
            'nativeRoleId': nativeRoleId,
            'nativeRoleSecret': nativeRoleSecret,
            'useAsDefault': useAsDefault,
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        native_role_data = response.json().get('nativeRole', {})
        return NativeRole(**native_role_data)

    def GetNativeRole(self, dataStoreId, nativeRoleId):
        url = f"{self.BASE_URL}/admin.v1.DataStoreService/GetNativeRole"
        payload = {
            'dataStoreId': dataStoreId,
            'nativeRoleId': nativeRoleId,
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        native_role_data = response.json().get('nativeRole', {})
        return NativeRole(**native_role_data)
