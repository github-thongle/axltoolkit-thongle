from axltoolkit import UcmPerfMonToolkit
from credentials import user, password, platform_user, platform_password
import json

ucm_ip = '172.18.106.58'

axl = UcmPerfMonToolkit(user, password, ucm_ip, False)

session_handle = axl.perfmonOpenSession()

counters = [
    "\\\\CHANGEME\\Cisco CallManager\\BandwidthAvailable",
    "\\\\CHANGEME\\Cisco CallManager\\BandwidthMaximum",
    "\\\\CHANGEME\\Cisco CallManager\\CallsInProgress",
    "\\\\CHANGEME\\Cisco CallManager\\CallsAttempted",
    "\\\\CHANGEME\\Cisco CallManager\\CallsCompleted"
]

result = axl.perfmonAddCounter(session_handle=session_handle, counters=counters)

if result is True:
    result = axl.perfmonCollectSessionData(session_handle=session_handle)
else:
    result = "Error adding perfmon counter"


new_result = []
for counter in result:
    category = counter.Name._value_1.split('\\')[-1]
    ipAddress = counter.Name._value_1.split('\\')[2]
    new_dict = {'category': category, 'ipAddress': ipAddress, 'value': counter.Value, 'cStatus': counter.CStatus}
    new_result.append(new_dict)

print(json.dumps(new_result))

result = axl.perfmonCloseSession(session_handle=session_handle)