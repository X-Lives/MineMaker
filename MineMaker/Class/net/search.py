import requests

class Search:
    def __init__(self, url):
        if url == "":
            self.url = 'https://mod.mcimirror.top'
        else:
            self.url = url
        self.modrinth = self.url + "/modrinth/v2/"
        self.curseforge = self.url + "/curseforge/v1/"
        self.mod_list = []
        self.mod_id_list = []
        self.index = None
        self.query = None
    def return_list(self, query, index):
        if index == 'r':
            self.index = 'relevance'
        elif index == 'd':
            self.index = 'downloads'
        elif index == 'f':
            self.index = 'follows'
        elif index == 'n':
            self.index = 'newest'
        elif index == 'u':
            self.index = 'updated'
        else:
            # default.
            self.index = 'relevance'
        self.query = query
        mod_list, mod_id_list = self.get_mod_id()
        return mod_list, mod_id_list
    def get_mod_id(self):
        for i in range(0, 10):
            try:
                response = requests.get(self.modrinth + 'search' + '?' + 'query=' + self.query + '&' + 'limit=10' + '&' + 'index=' + self.index)
                response.raise_for_status()
                data = response.json()
                if data['hits']:
                    self.mod_list.append(data['hits'][i]['title'])
                    self.mod_id_list.append(data['hits'][i]['project_id'])
            except requests.exceptions.RequestException as e:
                print(f"Error fetching mod info: {e}")
                break
        return self.mod_list, self.mod_id_list