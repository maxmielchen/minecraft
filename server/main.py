
from json import JSONDecoder, load
from typing import List
from docker import from_env as docker_env

from lib.image import Image
from lib.runtime import Runtime
from lib.runtimepool import RuntimePool
from lib.server import Server
from lib.serverpool import ServerPool

from threading import Thread

if __name__ == '__main__':
    with open("matrix.json") as matrix:
        data : JSONDecoder = load(matrix)
        runtimes = RuntimePool(data)
        servers = ServerPool(data)

        images = []

        for server in servers.servers:
            for runtime in runtimes.filtered_pool(server.get_java_version()):
                images.append(Image(server, runtime))

        docker_client = docker_env()

        threads: List[Thread] = []

        for image in images:
            threads.append(
                Thread(target=(Image.build(image, docker_client, True)))
            )

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
