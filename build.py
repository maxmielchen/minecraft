import json
import docker
from tqdm import tqdm


def main():
    print("Start matrix build...")
    with open("matrix.json") as mj:
        data = json.load(mj)

        runtime_version_list = data["runtime"]
        runtimes = []
        print("Load runtimes...")
        for runtime_version_key, runtime_version_value in tqdm(runtime_version_list.items()):
            version = runtime_version_key
            runtimes_list = runtime_version_value
            for runtime in runtimes_list:
                runtimes.append((version, runtime))

        
        try:
            print("Connect to docker engine...")
            docker_client = docker.from_env()
            docker_version = docker_client.version()
            docker_info = docker_client.info()
            docker_ping = docker_client.ping()
            print(" --Docker-- ")
            print(f"Info: {docker_info}")
            print(f"Version: {docker_version}")
            print(f"Ping: {docker_ping}")
            print(docker_ping)
            print(" --Docker-- ")
        except Exception:
            print("\033[91mCOULD NOT CONNECT TO DOCKER!")
            exit(1)

        server_type_list = data["server"]
        for server_type_key, server_type_value in tqdm(server_type_list.items()):
            server_type_name = server_type_key
            server_list = server_type_value
            for server in server_list:
                server_version = server["version"]
                server_source = server["source"]
                server_artifact = server["artifact"]
                java = server["java"]
                filtered_runtimes = [(v, r) for (v, r) in runtimes if v >= java]

                for runtime_version, runtime_properties in filtered_runtimes:
                    runtime_name = runtime_properties["name"]
                    image = runtime_properties["image"]

                    builded_image, logs = docker_client.images.build(
                        dockerfile="./Dockerfile",
                        path=".",
                        tag=f"minecraft:{server_type_name}-{server_version}-{runtime_name}-{runtime_version}",
                        nocache=True,
                        buildargs={
                            'source': server_source,
                            'artifact': server_artifact,
                            'image': image
                        }
                    )

                    builded_image.tag(registry="ghcr.io", repository="maxmielchen/minecraft", tag=f"{server_type_name}-{server_version}-{runtime_name}-{runtime_version}")
                    docker_client.images.push(repository='ghcr.io/maxmielchen/minecraft', tag=f"{server_type_name}-{server_version}-{runtime_name}-{runtime_version}")


if __name__ == '__main__':
    main()
