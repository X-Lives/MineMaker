import pyperclip
import keyboard
import time
import Function.tools as tools

Config = tools()

class Keyboard:
    def __init__(self):
        pass
    def get_selected_text(self):
        keyboard.press('ctrl+c')
        time.sleep(0.3)
        keyboard.release('ctrl+c')
        return pyperclip.paste()
    def on_hotkey(self):
        time.sleep(0.2)
        selected_text = self.get_selected_text()
        print(f"Chhoosed text: {selected_text}")
        return selected_text
    def start(self):
        keyboard.add_hotkey('ctrl+shift+h', self.on_hotkey)
        print("按下 Ctrl+Shift+H 来获取选中的内容...")
        keyboard.wait('esc')  # 等待用户按下 Esc 键来结束程序