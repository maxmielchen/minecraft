
from json import JSONDecoder, load
from typing import List
from docker import from_env as docker_env

from lib.image import Image
from lib.runtimepool import RuntimePool
from lib.serverpool import ServerPool

from multiprocessing import Pool

if __name__ == '__main__':
    with open("matrix.json") as matrix:
        data: JSONDecoder = load(matrix)                        # Loads the data stored in json
        runtimes = RuntimePool(data)                            # Gets all runtimes from the json
        servers = ServerPool(data)                              # Gets all servers from the json

        images: List[Image] = []                                # Holds all possible images

        for server in servers.get_runtimes():
            for runtime in runtimes.filtered_pool(server.get_java_version()):
                images.append(Image(server, runtime))           # Adds a supported image cross combination to the list

        docker_client = docker_env()                            # Connects to the docker engine

        with Pool(processes=16) as pool:

            results = []

            for image in images:
                result = pool.apply_async(image.build, (docker_client,))
                results.append(result)

            pool.close()
            pool.join(5.8 * 60 * 60)

            if not all(result.ready() for result in results):
                print("Couldn't finish building!")              # Sends a message if not all images could be built

            Image.push(docker_client)                           # Loads all images to the docker engine
