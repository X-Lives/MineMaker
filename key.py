import pyperclip
import keyboard
import time  
import threading
import Function.modpack as modpack
import Function.tools as tools

Config = tools.Config()

def get_selected_text():
    keyboard.press('ctrl+c')
    time.sleep(0.3)
    keyboard.release('ctrl+c')
    return pyperclip.paste()

def handle_selected_text(selected_text):
    modpack.main_keyboard(selected_text)

def on_hotkey():
    time.sleep(0.2)
    selected_text = get_selected_text()
    print(f"Chosen text: \033[1m{selected_text}\033[0m")
    # Create a new thread to handle modpack.main_keyboard
    thread = threading.Thread(target=handle_selected_text, args=(selected_text,))
    thread.start()

def main():
    keyboard.add_hotkey(Config.get('Key'), on_hotkey)
    print("Push \033[1mCtrl+Shift+H\033[0m to get the selected content...")
    keyboard.wait('esc')

if __name__ == '__main__':
    main()
