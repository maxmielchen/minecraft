from .server import Server
from .runtime import Runtime
from docker import DockerClient
from .env import BaseEnvironments

class Image:

    base_environments = BaseEnvironments()

    def __init__(self, server: Server, runtime: Runtime):
        self.server: Server = server
        self.runtime: Server = runtime

    def build(self, docker_client: DockerClient, instant: bool = False):
        builded_image, _ = docker_client.images.build(
            dockerfile="./Dockerfile",
            path=".",
            nocache=False,
            cache_from=[
                f"{self.base_environments.get_registry()}/{self.base_environments.get_repository()}:{self.server.server}-{self.server.version}-{self.runtime.name}-{self.runtime.java_version}-latest"
            ],
            buildargs={
                'http_source': self.server.source,
                'image': self.runtime.image
            }
        )
        builded_image.tag(repository=f"{self.base_environments.get_registry()}/{self.base_environments.get_repository()}", tag=f"{self.server.server}-{self.server.version}-{self.runtime.name}-{self.runtime.java_version}-latest")
        builded_image.tag(repository=f"{self.base_environments.get_registry()}/{self.base_environments.get_repository()}", tag=f"{self.server.server}-{self.server.version}-{self.runtime.name}-{self.runtime.java_version}-{self.base_environments.get_release_tag()}")

        if instant:
            docker_client.images.push(repository=f"{self.base_environments.get_registry()}/{self.base_environments.get_repository()}")
