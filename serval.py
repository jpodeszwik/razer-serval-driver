from evdev import UInput, AbsInfo, InputDevice
from evdev import ecodes as e
import evdev
from config import key_left, key_right, key_up, key_down, key_a, key_b, key_x, key_y, key_lt, key_lb, key_rt, key_rb


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
            self.ui.write(e.EV_KEY, key_left, 1)
        elif event.value == 1:
            self.ui.write(e.EV_KEY, key_right, 1)
        else:
            self.ui.write(e.EV_KEY, key_right, 0)
            self.ui.write(e.EV_KEY, key_left, 0)

        self.ui.syn()

    def up_down_event(self, event):
        if event.value == -1:
            self.ui.write(e.EV_KEY, key_up, 1)
        elif event.value == 1:
            self.ui.write(e.EV_KEY, key_down, 1)
        else:
            self.ui.write(e.EV_KEY, key_up, 0)
            self.ui.write(e.EV_KEY, key_down, 0)

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
            self.ui.write(e.EV_KEY, key_left, 1)
        elif event.value > 128 + self.delta:
            self.ui.write(e.EV_KEY, key_right, 1)
        else:
            self.ui.write(e.EV_KEY, key_right, 0)
            self.ui.write(e.EV_KEY, key_left, 0)

        self.ui.syn()

    def up_down_event(self, event):
        if event.value < 128 - self.delta:
            self.ui.write(e.EV_KEY, key_up, 1)
        elif event.value > 128 + self.delta:
            self.ui.write(e.EV_KEY, key_down, 1)
        else:
            self.ui.write(e.EV_KEY, key_up, 0)
            self.ui.write(e.EV_KEY, key_down, 0)

        self.ui.syn()


class AnalogStick2Processor:
    def __init__(self, ui):
        self.ui = ui
        self.d = 3

    def process_event(self, event):
        if event.type == 3:
            if event.code == 2:
                self.left_right_event(event)
            elif event.code == 5:
                self.up_down_event(event)

    def left_right_event(self, event):
        if event.value < 128:
            self.ui.write(e.EV_REL, e.REL_X, -self.d)
        elif event.value > 128:
            self.ui.write(e.EV_REL, e.REL_X, self.d)

        self.ui.syn()

    def up_down_event(self, event):
        if event.value < 128:
            self.ui.write(e.EV_REL, e.REL_Y, -self.d)
        elif event.value > 128:
            self.ui.write(e.EV_REL, e.REL_Y, self.d)

        self.ui.syn()


class AnalogButtonProcessor:
    def __init__(self, ui, input_code, output_code):
        self.delta = 20
        self.ui = ui
        self.input_code = input_code
        self.output_code = output_code

    def process_event(self, event):
        if event.type == 3:
            if event.code == self.input_code:
                if event.value > self.delta:
                    self.ui.write(e.EV_KEY, self.output_code, 1)
                else:
                    self.ui.write(e.EV_KEY, self.output_code, 0)

                self.ui.syn()


def LTButtonProcessor(ui):
    return AnalogButtonProcessor(ui, 10, key_lt)


def RTButtonProcessor(ui):
    return AnalogButtonProcessor(ui, 9, key_rt)


class SingleButtonProcessor:
    def __init__(self, ui, input_code, output_code):
        self.ui = ui
        self.input_code = input_code
        self.output_code = output_code

    def instance(self, ui):
        self.ui = ui
        return self

    def process_event(self, event):
        if event.type == 1:
            if event.code == self.input_code:
                if event.value == 1:
                    self.ui.write(e.EV_KEY, self.output_code, 1)
                elif event.value == 0:
                    self.ui.write(e.EV_KEY, self.output_code, 0)

                self.ui.syn()


def AButtonProcessor(ui):
    return SingleButtonProcessor(ui, 304, key_a)


def BButtonProcessor(ui):
    return SingleButtonProcessor(ui, 305, key_b)


def XButtonProcessor(ui):
    return SingleButtonProcessor(ui, 307, key_x)


def YButtonProcessor(ui):
    return SingleButtonProcessor(ui, 308, key_y)


def LBButtonProcessor(ui):
    return SingleButtonProcessor(ui, 310, key_lb)


def RBButtonProcessor(ui):
    return SingleButtonProcessor(ui, 311, key_rb)


def find_razer_serval():
    devices = [InputDevice(fn) for fn in evdev.list_devices()]

    for device in devices:
        if device.name == 'Razer Razer Serval':
            return device

    return None


def main():
    cap = {
        e.EV_KEY: [key_a, key_b, key_x, key_y, key_lt, key_rt, key_rb, key_lb, key_up, key_down, key_left, key_right],
        e.EV_REL: [
            (e.REL_Y, AbsInfo(0, 0, 255, 0, 0, 0)),
            (e.REL_X, AbsInfo(0, 0, 255, 0, 0, 0))
            ]
        }
    ui = UInput(cap, name='razer-serval-virtual-device')
    dev = find_razer_serval()

    event_processor_classes = [ArrowEventProcessor, AnalogStickProcessor, AButtonProcessor, BButtonProcessor,
                               XButtonProcessor, YButtonProcessor, LBButtonProcessor, RBButtonProcessor,
                               LTButtonProcessor, RTButtonProcessor, AnalogStick2Processor]
    event_processors = []

    for event_processor_class in event_processor_classes:
        event_processors.append(event_processor_class(ui))

    if dev is not None:
            for event in dev.read_loop():
                for processor in event_processors:
                    processor.process_event(event)


if __name__ == '__main__':
    main()
