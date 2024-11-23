import os
import time
import subprocess
import requests
import shutil
import Function.tools as tools

CVersions = tools.CompareVersions()
Config = tools.Config()

# 获取 Modrinth 上的 Mod URL
def get_mod_url(mod_name):
    url = f"https://api.modrinth.com/v2/search?query={mod_name}&limit=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，抛出异常
        data = response.json()
        if data['hits']:
            # 返回第一个匹配的 mod 的 URL 和 slug
            mod_slug = data['hits'][0]['slug']
            return f"https://modrinth.com/mod/{mod_slug}", mod_slug
        else:
            print(f"Mod '{mod_name}' not found on Modrinth.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mod info: {e}")
        return None, None

# 获取符合条件的 Mod 版本
def get_latest_mod_version(mod_slug):
    url = f"https://api.modrinth.com/v2/project/{mod_slug}/version"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，抛出异常
        versions = response.json()

        Game_Version_Range_Start = Config.get('Game_Version_Range_Start')
        Game_Version_Range_End = Config.get('Game_Version_Range_End')
        Platfrom = Config.get('Platform').strip().lower()

        # 筛选符合条件的版本
        for version in versions:
            if Platfrom in version['loaders']:
                for i in range(len(version['game_versions'])):
                    if CVersions.check_version(Game_Version_Range_Start, Game_Version_Range_End, version['game_versions'][i]):
                        return version
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mod versions: {e}")
        return None

# 下载 Mod 文件
def download_mod(version, mod_slug):
    # 获取下载链接
    download_url = version['files'][0]['url']
    file_name = version['files'][0]['filename']
    mods_dir = "Mods"

    # 创建 Mods 文件夹，如果不存在
    if not os.path.exists(mods_dir):
        os.makedirs(mods_dir)

    # 下载文件
    file_path = os.path.join(mods_dir, file_name)
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"\033[32mDownloaded\033[0m mod to \033[1m{file_path}\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"\033[31mError downloading mod: {e}\033[0m")

# 将 mod 信息追加到 Markdown 文件
def append_to_md_file(name, url, version_number="N/A", filename="mod_list.md"):
    with open(filename, "a") as file:
        file.write(f"- [{name}]({url}) | v{version_number}\n")

# 打开 mod_list.md 文件
def open_md_file(filename="mod_list.md"):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, filename)

    try:
        if os.name == 'nt':  # Windows 系统
            subprocess.run(['start', 'notepad', file_path], check=True, shell=True)
        elif os.name == 'posix':  # macOS / Linux 系统
            subprocess.run(['open', file_path], check=True)
        else:
            print("\033[31mUnsupported OS\033[0m")
    except Exception as e:
        print(f"\033[31mError opening file: {e}\033[0m")

# Main Program
def main():
    while True:
        # Get user input mod name.
        name = input("Input...\nName: ").strip()

        # Get mod URL.
        url, mod_slug = get_mod_url(name)
        if url and mod_slug:
            # Get the latest eligible mod version.
            version = get_latest_mod_version(mod_slug)
            if version:
                # Download mod.
                download_mod(version, mod_slug)
                # Write mod information to Markdown file.
                version_number = version['version_number']
                append_to_md_file(name, url, version_number)
                print(f"\033[32mAdded: \033[1m[{name}]({url}) | v{version_number}\033[0m")

            else:
                print(f"\033[31mNo suitable version found for '{name}' with \033[1m{Config.get('Platform')}\033[0m platform and game version >= \033[1m{Config.get('Game_Version')}\033[0m.")
                break

        # Print the current content of the md file.
        print("\n\033[32mCurrent content of the md file:\033[0m")
        with open("mod_list.md", "r") as file:
            print(file.read())

        # Ask if continue.
        cont = input("\n\033[32mDo you want to add another mod? (yes/no):\033[0m ").strip().lower()
        if cont != "yes":
            break

    # Open md file at the end.
    # open_md_file()

def main_keyboard(selected_text):
    print(f"Selected text: \033[1m{selected_text}\033[0m / running...")
    start_time = time.perf_counter() # Time counter start.
    name = selected_text.strip()
    # Get Mod URL
    url, mod_slug = get_mod_url(name)
    if url and mod_slug:
        # Get the latest eligible mod version.
        version = get_latest_mod_version(mod_slug)
        if version:
            # Dowload Mod.
            download_mod(version, mod_slug)
            # Write mod information to Markdown file.
            version_number = version['version_number']
            append_to_md_file(name, url, version_number)
            print(f"\033[32mAdded\033[0m: \033[1m[{name}]({url}) | v{version_number}\033[0m")

        else:
            print(f"\033[31mNo suitable version found for '{name}' with \033[1m{Config.get('Platform')}\033[0m platform and game version >= \033[1m{Config.get('Game_Version')}\033[0m.")
    end_time = time.perf_counter() # Time counter end.
    print(f"Time elapsed: {end_time - start_time:.2f} seconds.")

def print_md_file():
    # Print the current content of the md file.
    print("\nCurrent content of the md file:")
    with open("mod_list.md", "r") as file:
        print(file.read())

if __name__ == "__main__":
    main()
