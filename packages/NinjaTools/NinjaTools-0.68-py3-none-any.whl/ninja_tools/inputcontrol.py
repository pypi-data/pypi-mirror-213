import ctypes
from time import sleep

import win32con as k
import win32gui


class InputControl:
    def __init__(self, handle=None, window_name=None):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

        if handle is None and window_name is not None:
            self.handle = win32gui.FindWindow(None, window_name)
        else:
            self.handle = handle

        self.key = k

    def send_to_window(self, option, key=None):
        if self.handle is None:
            raise ValueError("handle is not set, use set_handle(handle) method to set it.")

        window_foreground = self.user32.GetForegroundWindow()
        thread_current = self.kernel32.GetCurrentThreadId()
        thread_window = self.user32.GetWindowThreadProcessId(self.handle, None)

        self.user32.SetFocus(self.handle)
        self.user32.AttachThreadInput(thread_window, thread_current, True)

        if option == 1:  # Click
            self.user32.SendMessageA(self.handle, k.WM_LBUTTONDOWN, 0, 0)
            sleep(0.08)
            self.user32.SendMessageA(self.handle, k.WM_LBUTTONUP, 0, 0)

        elif option == 2:  # Press
            self.user32.SendMessageA(self.handle, k.WM_KEYDOWN, key, 0)
            sleep(0.08)
            self.user32.SendMessageA(self.handle, k.WM_KEYUP, key, 0)

        elif option == 3:  # Press + Click
            self.user32.SendMessageA(self.handle, k.WM_KEYDOWN, key, 0)
            sleep(0.08)
            self.user32.SendMessageA(self.handle, k.WM_KEYUP, key, 0)
            sleep(0.08)
            self.user32.SendMessageA(self.handle, k.WM_LBUTTONDOWN, k.MK_LBUTTON, 0)
            sleep(0.1)
            self.user32.SendMessageA(self.handle, k.WM_LBUTTONUP, k.MK_LBUTTON, 0)
            sleep(0.09)

        elif option == 4:  # Combo Keys
            # Check if key is a list
            if not isinstance(key, list):
                raise TypeError('key must be a list')

            self.user32.SendMessageA(self.handle, k.WM_KEYDOWN, key[0], 0)
            sleep(0.08)
            self.user32.SendMessageA(self.handle, k.WM_KEYDOWN, key[1], 0)
            sleep(0.08)
            self.user32.SendMessageA(self.handle, k.WM_KEYUP, key[1], 0)
            sleep(0.08)
            self.user32.SendMessageA(self.handle, k.WM_KEYUP, key[0], 0)
            sleep(0.09)

        self.user32.AttachThreadInput(thread_window, thread_current, False)
        self.user32.SetFocus(window_foreground)
