import os
import json
import time
import Function.tools as tools

maz_check = tools.Check()
maz_get = tools.get()
maz_config = tools.Config()

class maz:
    def create_file(self, proj_name, pack_name, main_game_version, main_loaders):
        Timestamp = time.time()
        pack_maz = {'proj_name': proj_name, 'pack_name': pack_name, 'pack_version': '', 'pack_time': Timestamp, 'modify_times': '', 'bak_times': '', 'main_game_version': main_game_version, 'main_loaders': main_loaders, 'enable_multiple_versions': False, 'versions': {}}
        try:
            with open('pack.mz', 'w') as file:
                file.write(json.dumps(pack_maz, indent=4))
            return True
        except:
            return False
    def create_proj(self, proj_name, pack_name, main_game_version, main_loaders):
        try:
            os.mkdir(proj_name)
            os.chdir(proj_name)
            self.create_file(proj_name, pack_name, main_game_version, main_loaders)
        except:
            print('Failed to create project.')
            return False
    def get_file(self):
        if self.check_file():
            with open('pack.mz', 'r') as file:
                pack_maz = json.loads(file.read())
                return pack_maz
        else:
            print('pack.mz file is unavailable.')
            return None
    def check_file(self):
        try:
            with open('pack.mz', 'r') as file:
                pack_maz = json.loads(file.read())
                if 'proj_name' in pack_maz.keys() and pack_maz['proj_name']!= '':
                    if 'pack_name' in pack_maz.keys() and pack_maz['pack_name']!= '':
                        if 'pack_version' in pack_maz.keys():
                            if 'pack_time' in pack_maz.keys():
                                if 'modify_times' in pack_maz.keys():
                                    if 'bak_times' in pack_maz.keys():
                                        if 'main_game_version' in pack_maz.keys():
                                            if 'main_loaders' in pack_maz.keys():
                                                main_loaders = pack_maz['main_loaders']
                                                valid_versions = ['Fabric', 'Forge', 'NeoForge', 'Quilt']
                                                if isinstance(main_loaders, list):
                                                    for version in main_loaders:
                                                        if version not in valid_versions:
                                                            return False
                                                elif isinstance(main_loaders, str):
                                                    if main_loaders not in valid_versions:
                                                        return False
                                                if 'enable_multiple_versions' in pack_maz.keys():
                                                    if'versions' in pack_maz.keys():
                                                        return True
                return False
        except:
            return None
    def clean(self):
        try:
            os.chdir('Mods')
            print(os.listdir('.'))
            print('Files Number:', len(os.listdir('.')))
            if input('Clean all files? (Y/n): ').upper().strip() == 'Y':
                for file in os.listdir('.'):
                    os.remove(file)
        except:
            print('Exit.')

class workspace(maz):
    def get_list(self, path):
        folder = maz_get.folders(path) 
        Proj = []
        for i in folder:
            os.chdir(path)
            os.chdir(i)
            if self.check_file():
                Proj.append(i)
        return Proj
    def change(self, proj_name):
        maz_config.change('Workspace', proj_name)

def main():
    m = maz()
    w = workspace()
    path = os.getcwd() + '\\Workspace'
    os.chdir(path)
    m.create_proj('Test2', 'Test Pack2', '1.16.5', ['Fabric', 'Forge'])
    print(w.get(path))

if __name__ == '__main__':    
    main()