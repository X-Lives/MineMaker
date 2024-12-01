import os
import json
import time
import subprocess
import requests
import shutil
import Function.tools as tools

CVersions = tools.CompareVersions()
Config = tools.Config()
Time_m = tools.Time_More()

url_origin = 'https://api.modrinth.com/v2/'
url_origin_cn = 'https://mod.mcimirror.top/modrinth/v2/'

# Get the Mod ID on Modrinth
def get_mod_id(mod_name):
    url = f"{url_origin_cn}search?query={mod_name}&limit=1" #cn mirror
    try:
        response = requests.get(url)
        response.raise_for_status()  # Throw an exception if the request fails.
        data = response.json()
        if data['hits']:
            # Returns the URL and slug of the first matching mod.
            id = data['hits'][0]['project_id']
            return id
        else:
            print(f"Mod '{mod_name}' not found on Modrinth.")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mod info: {e}")
        return None, None

# Check if the mod is eligible
def check_mod(mod_id):
    url = f"{url_origin_cn}project/{mod_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            Game_Version_Range_Start = Config.get('Game_Version_Range_Start')
            Game_Version_Range_End = Config.get('Game_Version_Range_End')
            Platfrom = Config.get('Platform').strip().lower()
            if Platfrom in data['loaders']:
                for i in range(len(data['game_versions'])):
                    if CVersions.check_version(Game_Version_Range_Start, Game_Version_Range_End, data['game_versions'][i]):
                        return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking mod: {e}")
        return None

# Get the mod info
def get_mod(mod_id):
    url = f"{url_origin_cn}project/{mod_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data:
            client_side = data['client_side']
            server_side = data['server_side']
            mod_slug = data['slug']
            title = data['title']
            return client_side, server_side, mod_slug, title, f"https://modrinth.com/mod/{mod_slug}", data
        else:
            return None, None, None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mod: {e}")
        return None, None, None, None, None, None

# Get the mod versions
# Difference from function: check_mod.
# - Get more detailed Version parameters instead of checking.
# - Can return the download address.
def get_mod_versions(mod_id):
    url = f"{url_origin_cn}project/{mod_id}/version"
    try:
        response = requests.get(url)
        response.raise_for_status()  # If the request fails, throw an exception.
        versions = response.json()

        Game_Version_Range_Start = Config.get('Game_Version_Range_Start')
        Game_Version_Range_End = Config.get('Game_Version_Range_End')
        Platfrom = Config.get('Platform').strip().lower()

        # Filter the versions that meet the conditions
        for version in versions:
            if Platfrom in version['loaders']:
                for i in range(len(version['game_versions'])):
                    if CVersions.check_version(Game_Version_Range_Start, Game_Version_Range_End, version['game_versions'][i]):
                        return version
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching mod versions: {e}")
        return None

def check_mod_dowload(version):
    file_name = version['files'][0]['filename']
    mods_dir = "Mods"

    # Create the Mods folder if it doesn't exist
    if not os.path.exists(mods_dir):
        os.makedirs(mods_dir)
        return None
    # Check if the mod is already downloaded
    file_path = os.path.join(mods_dir, file_name)
    if os.path.exists(file_path):
        print(f"\033[32mMod already downloaded\033[0m: \033[1m{file_path}\033[0m")
        return True
    else:
        return False

# Download the mod file
def download_mod(version):
    # Get the download link
    download_url = version['files'][0]['url']
    file_name = version['files'][0]['filename']
    mods_dir = "Mods"

    # Create the Mods folder if it doesn't exist
    if not os.path.exists(mods_dir):
        os.makedirs(mods_dir)

    # Download the file
    file_path = os.path.join(mods_dir, file_name)
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        print(f"\033[32mDownloaded\033[0m mod to \033[1m{file_path}\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"\033[31mError downloading mod: {e}\033[0m")

def category_mods(file_name, client_side, server_side):
    client_dir = "Client"
    server_dir = "Server"
    if not os.path.exists(client_dir):
        os.makedirs(client_dir)
    if not os.path.exists(server_dir):
        os.makedirs(server_dir)
    
    if client_side == "required" or client_side == "optional":
        shutil.copy('Mods\\' + file_name, client_dir)
    
    if server_side == "required" or server_side == "optional":
        shutil.copy('Mods\\' + file_name, server_dir)


# Append the mod information to the Markdown file
def append_to_md_file(title, url, client_side, server_side, version_number="N/A", filename="mod_list.md"):
    with open(filename, "a") as file:
        file.write(f"- [{title}]({url}) | v{version_number} | client-side: {client_side} server-side: {server_side}\n")

# Open mod_list.md file
def open_md_file(filename="mod_list.md"):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, filename)

    try:
        if os.name == 'nt':  # Windows system
            subprocess.run(['start', 'notepad', file_path], check=True, shell=True)
        elif os.name == 'posix':  # macOS / Linux system
            subprocess.run(['open', file_path], check=True)
        else:
            print("\033[31mUnsupported OS\033[0m")
    except Exception as e:
        print(f"\033[31mError opening file: {e}\033[0m")

def add_res(version, data):
    file_name = version['files'][0]['filename'].replace('.jar', '.json')
    res_dir = "Res"
    #i = 1

    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    #while os.path.exists(os.path.join(res_dir, file_name)):
    #    file_name = file_name + i
    #    i = i + 1
    with open(os.path.join(res_dir, file_name), 'w') as file:
        file.write(json.dumps(data, indent=4))

def main(selected_text):
    # print(f"Selected text: \033[1m{selected_text}\033[0m / running...")
    start_time = time.perf_counter() # Time counter start.
    name = selected_text.strip()
    # Get Mod URL
    mod_id = get_mod_id(name)
    if mod_id:
        if check_mod(mod_id):
            client_side, server_side, mod_slug, title, url, data = get_mod(mod_id)
            version = get_mod_versions(mod_id)
            if version:
                if not check_mod_dowload(version):
                    # Dowload Mod.
                    download_mod(version)
                    category_mods(version['files'][0]['filename'], client_side, server_side)
                    # Write mod information to Markdown file.
                    version_number = version['version_number']
                    append_to_md_file(title, url, client_side, server_side, version_number)
                    add_res(version, data)
                    print(f"\033[32mAdded\033[0m: \033[1m[{title}]({url}) | v{version_number} | client-side: {client_side} server-side: {server_side}\033[0m")
            else:
                print(f"\033[31mNo suitable version found for '{name}' with \033[1m{Config.get('Platform')}\033[0m platform and game version >= \033[1m{Config.get('Game_Version')}\033[0m.")
        else:
            print(f"\033[31mMod '{name}' is not eligible for the current game version.\033[0m")
    end_time = time.perf_counter() # Time counter end.
    print(f"Time elapsed: {Time_m.check(end_time, start_time)} seconds.")

def print_md_file():
    # Print the current content of the md file.
    print("\nCurrent content of the md file:")
    with open("mod_list.md", "r") as file:
        print(file.read())

if __name__ == "__main__":
    main()
