from .runtime import Runtime
from json import JSONDecoder
from typing import List

class RuntimePool:

    def __init__(self, matrix_json: JSONDecoder):
        self.runtimes: List[Runtime] = []
        for json_java_version, json_runtime_images in matrix_json["runtimes"].items():
            for json_runtime_image in json_runtime_images:
                self.runtimes.append(Runtime(json_runtime_image["name"], json_runtime_image["image"], int(json_java_version)))

    def filtered_pool(self, min_java_version: int) -> List[Runtime]:
        filtered_list = []
        for runtime in self.runtimes:
            if (Runtime.get_java_version(runtime)) >= (min_java_version):
                filtered_list.append(runtime)
        return filtered_list

    def get_runtimes(self) -> List[Runtime]:
        return self.runtimes
