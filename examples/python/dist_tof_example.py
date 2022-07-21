# Write your code here :-)
import hub, utime
from dist_tof import DIST


tof = DIST(hub.port.C, 0x2)
print(tof.GetFirmwareVersion())
print(tof.GetVendorName())
print(tof.GetDeviceId())

while True:
    distance = tof.get_distance_mm()
    print(distance)
