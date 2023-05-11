
import json
import docker

from objects import RuntimePool
from objects import ServerPool
from objects import Server
from objects import Image
from json import JSONDecoder

from multiprocessing import Process

if __name__ == '__main__':
    with open("matrix.json") as matrix:
        data : JSONDecoder = json.load(matrix)
        runtimes = RuntimePool(data)
        servers = ServerPool(data)

        images = [Image]

        for server in servers.servers:
            for runtime in RuntimePool.filtered_pool(runtimes, Server.get_java_version(server)):
                images.append(Image(server, runtime))

        docker_client = docker.from_env()

        processes = [Process]

        for image in images:
            processes.append(
                Process(target=(Image.build(image, docker_client, True)))
            )

        for process in processes:
            process.start()

        for process in processes:
            process.join()
