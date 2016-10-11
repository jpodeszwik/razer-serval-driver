from evdev import InputDevice
from evdev import UInput
from evdev import ecodes as e
import evdev

ui = UInput()

def find_razer_serval():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()] 

    for device in devices:
        if device.name == 'Razer Razer Serval':
            return device

    return None

dev = find_razer_serval()

if dev != None:
    for event in dev.read_loop():
        if event.type == 3:
            if event.code == 0:
                if event.value < 128:
                    print('left')
                    ui.write(e.EV_KEY, e.KEY_LEFT, 1)
                    ui.syn()
                elif event.value > 128:
                    print('right')
                    ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
                    ui.syn()
                else:
                    print('release')
                    ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
                    ui.write(e.EV_KEY, e.KEY_LEFT, 0)
                    ui.syn()
            elif event.code == 1:
                if event.value < 128:
                    print('left')
                    ui.write(e.EV_KEY, e.KEY_UP, 1)
                    ui.syn()
                elif event.value > 128:
                    print('right')
                    ui.write(e.EV_KEY, e.KEY_DOWN, 1)
                    ui.syn()
                else:
                    print('release')
                    ui.write(e.EV_KEY, e.KEY_UP, 0)
                    ui.write(e.EV_KEY, e.KEY_DOWN, 0)
                    ui.syn()
            elif event.code == 16:
                if event.value == -1:
                    print('left')
                    ui.write(e.EV_KEY, e.KEY_LEFT, 1)
                    ui.syn()
                elif event.value == 1:
                    print('right')
                    ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
                    ui.syn()
                else:
                    print('release')
                    ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
                    ui.write(e.EV_KEY, e.KEY_LEFT, 0)
                    ui.syn()
            elif event.code == 17:
                if event.value == -1:
                    print('left')
                    ui.write(e.EV_KEY, e.KEY_UP, 1)
                    ui.syn()
                elif event.value == 1:
                    print('right')
                    ui.write(e.EV_KEY, e.KEY_DOWN, 1)
                    ui.syn()
                else:
                    print('release')
                    ui.write(e.EV_KEY, e.KEY_UP, 0)
                    ui.write(e.EV_KEY, e.KEY_DOWN, 0)
                    ui.syn()

