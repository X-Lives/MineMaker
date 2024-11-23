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
        with open(f"Config/{ini}.ini", "r") as get_file:
            get_str = get_file.readline()
            get_str = get_str.replace("\n", "")
            return get_str
    def change(self, ini, change):
        with open(f"Config/{ini}.ini", "w") as change_file:
            change_file.write(change)