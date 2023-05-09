from json import JSONDecoder
from typing import Any, List
from docker import DockerClient
import env as env


class Runtime:

    def __init__(self, name: str, image: str, java_version: int):
        self.name = name
        self.image = image
        self.java_version = java_version

    def get_name(self) -> str:
        return self.name
    
    def get_image(self) -> str:
        return self.image
    
    def get_java_version(self) -> str:
        return self.java_version
    
    def info(self) -> str:
        return f"""
        #  - {self.get_name()} -
        # Java: {self.get_java_version()}
        """
    
class RuntimePool:

    def __init__(self, matrix_json: JSONDecoder):
        self.runtimes = [Runtime]
        for json_java_version, json_runtime_images in matrix_json["runtimes"].items():
            for json_runtime_image in json_runtime_images:
                self.runtimes.append(Runtime(json_runtime_image["name"], json_runtime_image["image"], int(json_java_version)))

    def filtered_pool(self, min_java_version: int) -> List[Runtime]:
        filtered_list = List[Runtime]
        for runtime in self.runtimes:
            if runtime.get_java_version(runtime) >= min_java_version:
                filtered_list.append(runtime)
        return filtered_list

    def get_runtimes(self) -> List[Runtime]:
        return self.runtimes

class Server:

    def __init__(self, server: str, version: str, source: str, java_version: int):
        self.server = server
        self.version = version
        self.source = source
        self.java_version = java_version

    def get_server(self) -> str:
        return self.server
    
    def get_version(self) -> str:
        return self.version
    
    def get_source(self) -> str:
        return self.source
    
    def get_java_version(self) -> int:
        return self.version
    
    def info(self) -> str:
        return f"""
        #  - {self.server} -
        # Version: {self.version}
        """

class ServerPool:

    def __init__(self, matrix_json: JSONDecoder):
        self.servers = [Server]
        for json_server_name, json_servers in matrix_json["servers"].items():
            for json_server in json_servers:
                self.servers.append(Server(json_server_name, json_server["version"], json_server["source"], json_server["java"]))

class Image:

    def __init__(self, server: Server, runtime: Runtime):
        self.server = server
        self.runtime = runtime

    def build(self, docker_client: DockerClient, instant: bool = False):
        builded_image, logs = docker_client.images.build(dockerfile="./Dockerfile",path=".",nocache=True,
            buildargs={
                'http_source': self.server.source,
                'image': self.runtime.image
            }
        )
        builded_image.tag(repository=f"{env.registry}/{env.repository}", tag=f"{self.server.server}-{self.server.version}-{self.runtime.name}-{self.runtime.java_version}-latest")
        builded_image.tag(repository=f"{env.registry}/{env.repository}", tag=f"{self.server.server}-{self.server.version}-{self.runtime.name}-{self.runtime.java_version}-{env.release_tag}")
        self.image  = builded_image
        self.logs = logs

        if instant:
            docker_client.images.push(repository=f"{env.registry}/{env.repository}")
