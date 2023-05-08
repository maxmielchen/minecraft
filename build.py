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
        for runtime_version_key, runtime_version_value in runtime_version_list.items():
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
        for server_type_key, server_type_value in server_type_list.items():
            server_type_name = server_type_key
            server_list = server_type_value
            for server in server_list:
                server_version = server["version"]
                server_source = server["source"]
                #server_artifact = server["artifact"]
                java = server["java"]

                #filtered_runtimes = [(v, r) for (v, r) in runtimes if v >= java] # Does not work


                for runtime_version, runtime_properties in filtered_runtimes:
                    runtime_name = runtime_properties["name"]
                    image = runtime_properties["image"]

                    print(f"Try to build -> minecraft:{server_type_name}-{server_version}-{runtime_name}-{runtime_version}")

                    builded_image, logs = docker_client.images.build(
                        dockerfile="./Dockerfile",
                        path=".",
                        tag=f"minecraft:{server_type_name}-{server_version}-{runtime_name}-{runtime_version}",
                        nocache=True,
                        buildargs={
                            'http_source': server_source,
                            'image': image
                        }
                    )

                    print(logs)

                    print(f"Successfully build -> minecraft:{server_type_name}-{server_version}-{runtime_name}-{runtime_version}")

                    builded_image.tag(repository="ghcr.io/maxmielchen/minecraft", tag=f"{server_type_name}-{server_version}-{runtime_name}-{runtime_version}")
                    docker_client.images.push(repository='ghcr.io/maxmielchen/minecraft', tag=f"{server_type_name}-{server_version}-{runtime_name}-{runtime_version}")

                    print(f"Successfully pushed -> minecraft:{server_type_name}-{server_version}-{runtime_name}-{runtime_version}")


if __name__ == '__main__':
    main()
