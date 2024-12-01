import pyperclip
import keyboard
import time
import os
import sys
import threading
import Function.modpack as modpack
import Function.tools as tools
import Function.maz as maz

Config = tools.Config()
maz = maz.maz()

def get_selected_text():
    keyboard.press('ctrl+c')
    time.sleep(0.3)
    keyboard.release('ctrl+c')
    return pyperclip.paste()

def handle_selected_text(selected_text):
    modpack.main(selected_text)

def on_hotkey():
    time.sleep(0.2)
    selected_text = get_selected_text()
    print(f"Chosen text: \033[1m{selected_text}\033[0m")
    # Create a new thread to handle modpack.main_keyboard
    thread = threading.Thread(target=handle_selected_text, args=(selected_text,)) 
    thread.start()

def main():
    main_path = os.getcwd()
    workspace = Config.get('Workspace')
    if workspace:
        os.chdir(main_path + '\\WorkSpace\\' + workspace)
    keyboard.add_hotkey(Config.get('Key'), on_hotkey)
    print("Push \033[1mCtrl+Shift+H\033[0m to get the selected content...")
    keyboard.wait('esc')

def clean():
    main_path = os.getcwd()
    workspace = Config.get('Workspace')
    if workspace:
        os.chdir(main_path + '\\WorkSpace\\' + workspace)
    maz.clean()

if __name__ == '__main__':
    if sys.argv[1] == 'clean':
        clean()
    else:
        main()
