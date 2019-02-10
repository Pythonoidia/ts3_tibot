import requests
from requests.auth import HTTPBasicAuth
import configuration


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

    def server_admins(self):
        server_admin = {}
        for clients in self.clients_info():
            for client in clients:
                if client["client_servergroups"] == '9':
                    server_admin[client["client_database_id"]] = client["cid"]
        return server_admin

    def kick_from_admin_channel(self):
        admin = self.server_admin()
        for user in self.client_list:
            if user["cid"] in admin.values() and user["client_database_id"] not in admin.keys():
                print(user["client_nickname"])
                requests.get(configuration.hg_kick.format(user["clid"]),auth=self.auth)
        return None

    def move_all_players(self):
        admin = self.server_admins()
        for user in self.client_list:
            if user["cid"] not in admin.values():
                requests.get(configuration.hg_move.format(admin.values(), user["clid"]), auth=self.auth)
        return None

def main():
    tb = TibBot()


if __name__ == '__main__':
    main()
