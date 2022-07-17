# Write your code here :-)
## TMP275: this class provides functions for TMP275Nx from mindsensors.com
#for read and write operations.
import hub,time
from mindsensors import TMP275
print("this is TMP275 test")



tmp = TMP275(hub.port.A)
while True:
    tmper =tmp.readTemperature()
    print("Temperature is ",tmper,u"\u2103")
    hub.display.show(str(tmper))
    time.sleep(1)
