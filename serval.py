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
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 1)
        elif event.value == 1:
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
        else:
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 0)

        self.ui.syn()

    def up_down_event(self, event):
        if event.value == -1:
            self.ui.write(e.EV_KEY, e.KEY_UP, 1)
        elif event.value == 1:
            self.ui.write(e.EV_KEY, e.KEY_DOWN, 1)
        else:
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
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 1)
        elif event.value > 128 + self.delta:
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 1)
        else:
            self.ui.write(e.EV_KEY, e.KEY_RIGHT, 0)
            self.ui.write(e.EV_KEY, e.KEY_LEFT, 0)

        self.ui.syn()

    def up_down_event(self, event):
        if event.value < 128 - self.delta:
            self.ui.write(e.EV_KEY, e.KEY_UP, 1)
        elif event.value > 128 + self.delta:
            self.ui.write(e.EV_KEY, e.KEY_DOWN, 1)
        else:
            self.ui.write(e.EV_KEY, e.KEY_UP, 0)
            self.ui.write(e.EV_KEY, e.KEY_DOWN, 0)

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
    return AnalogButtonProcessor(ui, 9, e.KEY_K)


def RTButtonProcessor(ui):
    return AnalogButtonProcessor(ui, 10, e.KEY_E)


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
    return SingleButtonProcessor(ui, 304, e.KEY_A)


def BButtonProcessor(ui):
    return SingleButtonProcessor(ui, 305, e.KEY_B)


def XButtonProcessor(ui):
    return SingleButtonProcessor(ui, 307, e.KEY_X)


def YButtonProcessor(ui):
    return SingleButtonProcessor(ui, 308, e.KEY_Y)


def LBButtonProcessor(ui):
    return SingleButtonProcessor(ui, 310, e.KEY_L)


def RBButtonProcessor(ui):
    return SingleButtonProcessor(ui, 311, e.KEY_R)


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

    event_processor_classes = [ArrowEventProcessor, AnalogStickProcessor, AButtonProcessor, BButtonProcessor,
                               XButtonProcessor, YButtonProcessor, LBButtonProcessor, RBButtonProcessor,
                               LTButtonProcessor, RTButtonProcessor]
    event_processors = []

    for event_processor_class in event_processor_classes:
        event_processors.append(event_processor_class(ui))

    if dev is not None:
            for event in dev.read_loop():
                for processor in event_processors:
                    processor.process_event(event)


if __name__ == '__main__':
    main()
