
class Runtime:
    "Holds data from a java runtime"

    def __init__(self, name: str, image: str, java_version: int):
        self.name: str = name
        self.image: str = image
        self.java_version: int = java_version

    def get_name(self) -> str:
        "Returns the name of the java runtime"
        return self.name
    
    def get_image(self) -> str:
        "Returns the image tag"
        return self.image
    
    def get_java_version(self) -> int:
        "Returns the java version"
        return self.java_version
    
    def info(self) -> str:
        "Returns an info batch"
        return f"""
        #  - {self.name} -
        # Java: {self.java_version}
        """
    