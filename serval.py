from evdev import UInput
from evdev import ecodes as e
import evdev


class ArrowEventProcessor:
    def __init__(self, ui):
        self.ui = ui

    def process_event(self, event):
        if event.type == 3:
            if event.code == 16:
                self.left_right_event(event)
            elif event.code == 17:
                self.up_down_event(event)

    def left_right_event(self, event):
        if event.value == -1:
            print('left')
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 1)
        elif event.value == 1:
            print('right')
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
        else:
            print('release')
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 0)

        self.ui.syn()

    def up_down_event(self, event):
        if event.value == -1:
            print('up')
            self.ui.write(e.EV_KEY, e.KEY_UP, 1)
        elif event.value == 1:
            print('down')
            self.ui.write(e.EV_KEY, e.KEY_DOWN, 1)
        else:
            print('release')
            self.ui.write(e.EV_KEY, e.KEY_UP, 0)
            self.ui.write(e.EV_KEY, e.KEY_DOWN, 0)

        self.ui.syn()


class AnalogStickProcessor:
    def __init__(self, ui):
        self.delta = 20
        self.ui = ui

    def process_event(self, event):
        if event.type == 3:
            if event.code == 0:
                self.left_right_event(event)
            elif event.code == 1:
                self.up_down_event(event)

    def left_right_event(self, event):
        if event.value < 128 - self.delta:
            print('left')
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 1)
        elif event.value > 128 + self.delta:
            print('right')
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
        else:
            print('release')
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 0)

        self.ui.syn()

    def up_down_event(self, event):
        if event.value < 128 - self.delta:
            print('up')
            self.ui.write(e.EV_KEY, e.KEY_UP, 1)
        elif event.value > 128 + self.delta:
            print('down')
            self.ui.write(e.EV_KEY, e.KEY_DOWN, 1)
        else:
            print('release')
            self.ui.write(e.EV_KEY, e.KEY_UP, 0)
            self.ui.write(e.EV_KEY, e.KEY_DOWN, 0)

        self.ui.syn()


def find_razer_serval():
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

    for device in devices:
        if device.name == 'Razer Razer Serval':
            return device

    return None


def main():
    ui = UInput()
    dev = find_razer_serval()
    print(dev)

    event_processors = [ArrowEventProcessor(ui), AnalogStickProcessor(ui)]

    if dev is not None:
        for event in dev.read_loop():
            for processor in event_processors:
                processor.process_event(event)


if __name__ == '__main__':
    main()