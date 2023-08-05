# From github: https://gist.github.com/pudquick/134acb5f7423312effcc98ec56679136

import objc
from Foundation import NSBundle

IOKit = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

functions = [("IOPSCopyPowerSourcesByType", b"@I")]

objc.loadBundleFunctions(IOKit, globals(), functions)

# matches information pulled by: pmset -g batt
def battery_dict():
    try:
        battery = list(IOPSCopyPowerSourcesByType(0))[0]
    except:
        battery = 0
    if battery != 0:
        # we have a battery
        return battery


def battery_percent():
    d = battery_dict()
    if d:
        return d["Current Capacity"]


def on_battery():
    d = battery_dict()
    if d:
        return d["Power Source State"] == "Battery Power"


if __name__ == '__main__':
    print(battery_dict())
    print(f'Battery: {battery_percent()}%')
    print('On battery power' if on_battery() else 'Connected to power')

