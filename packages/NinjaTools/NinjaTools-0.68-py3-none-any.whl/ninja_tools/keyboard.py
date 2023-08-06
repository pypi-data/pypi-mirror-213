import ctypes
from random import uniform
from time import sleep

import win32gui

import ninja_tools.keycodes as key

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004


class MOUSE_INPUT(ctypes.Structure):
    _fields_ = (('dx', ctypes.c_long),
                ('dy', ctypes.c_long),
                ('mouseData', ctypes.c_ulong),
                ('dwFlags', ctypes.c_ulong),
                ('time', ctypes.c_ulong),
                ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)))


class KEYBOARD_INPUT(ctypes.Structure):
    _fields_ = (('wVk', ctypes.c_ushort),
                ('wScan', ctypes.c_ushort),
                ('dwFlags', ctypes.c_ulong),
                ('time', ctypes.c_ulong),
                ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)))


class HARDWARE_INPUT(ctypes.Structure):
    _fields_ = (('uMsg', ctypes.c_ulong),
                ('wParamL', ctypes.c_ushort),
                ('wParamH', ctypes.c_ushort))


class _INPUT_union(ctypes.Union):
    _fields_ = (('mi', MOUSE_INPUT),
                ('ki', KEYBOARD_INPUT),
                ('hi', HARDWARE_INPUT))


class INPUT(ctypes.Structure):
    _fields_ = (('type', ctypes.c_ulong),
                ('union', _INPUT_union))


def send_input(*inputs):
    n_inputs = len(inputs)
    lp_input = INPUT * n_inputs
    p_inputs = lp_input(*inputs)
    cb_size = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(n_inputs, p_inputs, cb_size)


def input_structure(structure):
    if isinstance(structure, MOUSE_INPUT):
        return INPUT(INPUT_MOUSE, _INPUT_union(mi=structure))
    if isinstance(structure, KEYBOARD_INPUT):
        return INPUT(INPUT_KEYBOARD, _INPUT_union(ki=structure))
    if isinstance(structure, HARDWARE_INPUT):
        return INPUT(INPUT_HARDWARE, _INPUT_union(hi=structure))
    raise TypeError('Cannot create INPUT structure!')


def keyboard_input_unicode(code, flags=0):
    flags = KEYEVENTF_UNICODE | flags
    return KEYBOARD_INPUT(0, code, flags, 0, None)


def keyboard_input_vk(code, flags=0):
    return KEYBOARD_INPUT(code, code, flags, 0, None)


def keyboard_event_unicode(code, _):
    return input_structure(keyboard_input_unicode(code))


def keyboard_event_vk(code, flags=0):
    return input_structure(keyboard_input_vk(code, flags))


def is_pressed(code):
    return ctypes.windll.user32.GetKeyState(code) & 0x8000


def delay(min_delay=50, max_delay=100):
    sleep(uniform(min_delay / 1000, max_delay / 1000))


def key_down(code):
    send_input(keyboard_event_vk(code, flags=0))


def key_up(code):
    send_input(keyboard_event_vk(code, KEYEVENTF_KEYUP))


def press(code, pause=None):
    key_down(code)

    if pause:
        sleep(pause / 1000)
    else:
        delay()

    key_up(code)

    if pause:
        sleep(pause / 1000)
    else:
        delay()


def two_keys_combo(key1, key2):
    send_input(keyboard_event_vk(key1), keyboard_event_vk(key2))
    delay()
    send_input(keyboard_event_vk(key2, KEYEVENTF_KEYUP),
               keyboard_event_vk(key1, KEYEVENTF_KEYUP))
    delay()


def _press(character):
    unicode_to_vk = {
        '\r': 0x0D,
        '\n': 0x0D,
    }
    if character in unicode_to_vk:
        return press(unicode_to_vk[character])
    code = ord(character)
    send_input(keyboard_event_unicode(code, 0))
    delay()
    send_input(keyboard_event_unicode(code, KEYEVENTF_KEYUP))
    delay()


def type_stream(string):
    for char in string:
        _press(char)


class WindowPress:
    def __init__(self, handle=None, window_name=None, focus=True, foreground=True, attach=True):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.focus = focus
        self.foreground = foreground
        self.attach = attach

        if handle is None and window_name is not None:
            self.handle = win32gui.FindWindow(None, window_name)
        else:
            self.handle = handle

        self.key = key

    def press(self, key_code):
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        # Attach the current thread to the thread of the window you want to send input to
        window_foreground = user32.GetForegroundWindow()
        thread_current = kernel32.GetCurrentThreadId()
        thread_window = user32.GetWindowThreadProcessId(self.handle, None)

        if self.attach and thread_current != thread_window:
            user32.AttachThreadInput(thread_window, thread_current, True)

        if self.focus:
            user32.SetFocus(self.handle)

        if self.foreground:
            user32.SetForegroundWindow(self.handle)

        # Press key
        press(key_code)

        # Detach the current thread from the window

        if self.attach and thread_current == thread_window:
            user32.AttachThreadInput(thread_window, thread_current, False)

        if self.focus:
            user32.SetFocus(window_foreground)

        if self.foreground:
            user32.SetForegroundWindow(window_foreground)
