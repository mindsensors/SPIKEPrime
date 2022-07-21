# Write your code here :-)
import hub,time
from EV3Flow import EV3FLOW
flow = EV3FLOW(hub.port.C)

print(flow.GetFirmwareVersion())
print(flow.GetVendorName())
print(flow.GetDeviceId())
while True:
    print(flow.get_volume(),flow.get_flow())
    time.sleep(1)

