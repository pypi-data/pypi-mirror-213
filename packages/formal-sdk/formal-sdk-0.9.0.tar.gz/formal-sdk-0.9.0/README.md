# Formal Admin Python SDK


This is the Python SDK for the Formal Admin API.



## Installing
    pip install formal-sdk

## Example Use

Create and Get a Native Role

```python
import os
import formal_sdk

if __name__ == '__main__':

    dataStoreId = ""
    nativeRoleId = ""
    nativeRoleSecret = ""
    useAsDefault = True
    apiKey = os.environ.get('TEST_API_KEY')
    
    newClient = formal_sdk.Client(apiKey)
    # Create Native Role
    createdRole = newClient.DataStoreClient.CreateNativeRole(dataStoreId=dataStoreId, nativeRoleId=nativeRoleId, nativeRoleSecret=nativeRoleSecret, useAsDefault=useAsDefault)
    
    # Get Native Role    
    previousRole = newClient.DataStoreClient.GetNativeRole(dataStoreId=dataStoreId, nativeRoleId=nativeRoleId)

    print(f'DataStoreId: {previousRole.dataStoreId}')
    print(f'NativeRoleId: {previousRole.nativeRoleId}')
    print(f'NativeRoleSecret: {previousRole.nativeRoleSecret}')
    print(f'UseAsDefault: {previousRole.useAsDefault}')

    # Get sidecar tls certificate and private key
    sidecarId = ""
    certificate, privateKey, fullSecret = newClient.SidecarClient.GetTLSCertificate(sidecarId)
```