# Write your code here :-)
import hub, time
from Sumoeyes import SUMOEYES


sumo = SUMOEYES(hub.port.A)
print(sumo.GetFirmwareVersion())
print(sumo.GetHardwareVersion())


while True:

    print(sumo.read())
    time.sleep(0.3)
