# Write your code here :-)
import hub, time
from  projects.lib.mindsensors  import IRTHERMO


irt = IRTHERMO(hub.port.C)
print(irt.GetFirmwareVersion())
print(irt.GetVendorName())
print(irt.GetDeviceId())

while True:
    # print(irt.get_AmbientC())
    # print(irt.get_AmbientF())
    print(irt.get_TargetC(), irt.get_AmbientC())
    # print(irt.get_TargetF())
    time.sleep(1)
