# Write your code here :-)

import hub,time
from projects.lib.mindsensors import TMP275




tmp = TMP275(hub.port.C)
print("this is TMP275 test")
while True:
    tmper =tmp.readTemperature()
    print("Temperature is ",tmper,u"\u2103")
    hub.display.show(str(tmper))
    time.sleep(1)
