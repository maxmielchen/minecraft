
from json import JSONDecoder, load
from typing import List
from docker import from_env as docker_env

from lib.image import Image
from lib.runtime import Runtime
from lib.runtimepool import RuntimePool
from lib.server import Server
from lib.serverpool import ServerPool

from threading import Thread
from multiprocessing import Pool, Semaphore
from multiprocessing.pool import AsyncResult

if __name__ == '__main__':
    with open("matrix.json") as matrix:
        data : JSONDecoder = load(matrix)
        runtimes = RuntimePool(data)
        servers = ServerPool(data)

        images: List[Image] = []

        for server in servers.servers:
            for runtime in runtimes.filtered_pool(server.get_java_version()):
                images.append(Image(server, runtime))

        docker_client = docker_env()

        with Pool(processes=16) as pool:

            semaphore = Semaphore(0)

            for image in images:
                pool.apply_async(image.build, (docker_client,), callback=semaphore.release)

            semaphore.acquire(block=True)

            """
            single_build = lambda image: image.build(docker_client)

            result = pool.map_async(single_build, images)
        
            result.wait()
            result.successful()

            pool.close()
            pool.join()

            ---
            
            results: List[AsyncResult] = []
            for thread in threads:
                results.append(pool.apply_async(func=thread.start))

            pool.close()
            pool.join()
            """

        Image.push(docker_client)
