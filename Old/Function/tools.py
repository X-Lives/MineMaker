import os

# Compare Versions
class CompareVersions:
    def compare_versions(self,version1, version2):
        # Can't compare versions if they are not numbers.
        # e.g. 23w43a/b | 1.20.5-pre1
        try:
            v1 = list(map(int, version1.split('.')))
            v2 = list(map(int, version2.split('.')))
            if v1 >= v2:
                return True
            elif v1 < v2:
                return False
        except:
            return False
    def check_version(self, version1, version2, version3):
        # Can't compare versions if they are not numbers.
        # e.g. 23w43a/b | 1.20.5-pre1
        # v1: Start Version | v2: End Version | v3: Current Version
        try:
            v1 = list(map(int, version1.split('.')))
            v2 = list(map(int, version2.split('.')))
            v3 = list(map(int, version3.split('.')))
            if v3 >= v1 and v3 <= v2:
                return True
            else:
                return False
        except:
            return False

# Read or Write Config File
class Config:
    def __init__(self):
        self.current_dir = os.getcwd()
    def get(self, ini):
        with open(self.current_dir + f"\\Config\\{ini}.ini", "r") as get_file:
            get_str = get_file.readline()
            get_str = get_str.replace("\n", "")
            return get_str
    def change(self, ini, change):
        with open(self.current_dir + f"\\Config\\{ini}.ini", "w") as change_file:
            change_file.write(change)

class Check:
    def file(self, file_path):
        if os.path.exists(file_path):
            return True
        else:
            return False
    def dir(self, dir_path):
        if os.path.isdir(dir_path):
            return True
        else:
            return False

class get:
    def folders(self, directory):
        folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
        if len(folders) == 0:
            print('Error found folders')
            return None
        else:
            return folders

class Time_More:
    def check(self, end_time, start_time):
        duration = end_time - start_time
        if duration < 5:
            return f"\033[0;32m{duration:.2f}\033[0m"
        elif duration < 10:
            return f"\033[0;33m{duration:.2f}\033[0m"
        elif duration < 20:
            return f"\033[0;31m{duration:.2f}\033[0m"
        else:
            print(f"\033[1;33mWARN\033[0m | {duration} is too long!")
            return f"{duration:.2f}\033[0m"