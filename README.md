# Airwatch

Script to sync VMWare AirWatch to Device42 (http://device42.com). Tested against AirWatch 9.5.0.2 and Device42 15.06.00.

Current script version migrate `devices, ips, macs and software` data. If you have any requests\improvements, feel free to contact us.

## Authentication
The AirWatch to Device42 sync authenticates to the AirWatch RESTful interface using Basic Authentication. This requires the user name and password of an admin account with API access, and an API key.

### To enable Basic Authentication in AirWatch
1. Go to 'Groups & Settings' → 'All Settings' → 'System' → 'Advanced' → 'API' → 'REST API'
2. Under the General Tab, verify 'Enable API Access' is 'Enabled'
3. Select the 'Authentication' Tab and set 'Basic' to 'Enabled'

### To retrieve API Key
1. Go to 'Groups & Settings' → 'All Settings' → 'System' → 'Advanced' → 'API' → 'REST API'
2. Under the General Tab, select 'ADD'.
3. Name a service, choose 'Admin' and save the API Key for the AirWatch to Device42 sync.

### AirWatch to Device42 Sync Configuration
1. `pip install -r requirements.txt`
2. Rename config.yaml.example to config.yaml. Update settings that match your environment.

### AirWatch to Device42 Sync Execution
`python sync.py`

