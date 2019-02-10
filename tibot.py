import requests
from requests.auth import HTTPBasicAuth
import configuration
import pprint

class TibBot(object):
    def __init__(self):
        self.auth = HTTPBasicAuth(configuration.api_login, configuration.api_password)
        self.client_list = requests.get(configuration.hg_clients, auth=self.auth).json()

    def clid_list(self):
        clid_list = []
        for clients in self.client_list:
            clid_list.append((clients["clid"]))
        return clid_list

    def mass_poke(self):
        client_list = self.client_list
        for clients in client_list:
            requests.get(configuration.hg_poke.format('zaloga hellgate.pl zyczy milego dnia', int(clients["clid"])),
                    auth=self.auth)
        return None

    def mass_kick(self):
        client_list = self.client_list
        for clients in client_list:
            requests.get(configuration.hg_kick.format(clients["clid"]), auth=self.auth)
        return None

    def clients_info(self):
        clid_list = self.clid_list()
        clients_information = []
        for clients in clid_list:
            clients_information.append(requests.get(configuration.hg_client_info.format(clients), auth=self.auth).json())
        return clients_information

    def kick_from_admin_channel(self):
        clid_list = self.clid_list()
        for user in clid_list:
            if  



def main():
    tb = TibBot()
    #tb.mass_poke()
    #print(tb.clid_list())
    pprint.pprint(tb.clients_info())

if __name__ == '__main__':
    main()
