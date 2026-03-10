import key
import time
import Function.tools as tools

main_config = tools.Config()

text=f'''
\033[33m⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[0m   |  \033[1m〽Mine Maker\033[0m
\033[33m⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿\033[0m   |  by: Is52hertz
\033[33m⣿⣿⣿⠀⠀⠀⠙⢿⣿⣿⣿⣿⡿⠋⠀⠀⠀⣿⣿⣿\033[0m   |  ---------
\033[33m⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⠟⠀⠀⠀⠀⠀⣿⣿⣿\033[0m   |  Version: {main_config.get("Version")}
\033[33m⣿⣿⣿⠀⠀⠀⡀⠀⠀⠙⠃⠀⠀⢀⠀⠀⠀⣿⣿⣿\033[0m   |  Time: {time.strftime("%Y-%m-%d %H:%M:%S")}
\033[33m⣿⣿⣿⠀⠀⠀⣿⣆⠀⠀⠀⠀⣰⣯⠀⠀⠀⣿⣿⣿\033[0m
\033[33m⣿⣿⣿⠀⠀⠀⣿⣿⣷⣤⣤⣾⣿⣿⠀⠀⠀⣿⣿⣿\033[0m
\033[33m⣿⣿⣿⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⣿⣿\033[0m
\033[33m⣿⣿⣿⣷⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿\033[0m
\033[33m⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[0m'''

# Under construction...
def main():
    print(text)
    key.main()

if __name__ == '__main__':
    main()

