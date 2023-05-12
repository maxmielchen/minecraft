from typing import List
from .server import Server
from json import JSONDecoder

class ServerPool:

    def __init__(self, matrix_json: JSONDecoder):
        self.servers: List[Server] = []
        for json_server_name, json_servers in matrix_json["servers"].items():
            for json_server in json_servers:
                self.servers.append(Server(json_server_name, json_server["version"], json_server["source"], json_server["java"]))
