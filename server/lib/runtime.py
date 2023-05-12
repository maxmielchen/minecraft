
class Runtime:

    def __init__(self, name: str, image: str, java_version: int):
        self.name: str = name
        self.image: str = image
        self.java_version: int = java_version

    def get_name(self) -> str:
        return self.name
    
    def get_image(self) -> str:
        return self.image
    
    def get_java_version(self) -> int:
        return self.java_version
    
    def info(self) -> str:
        return f"""
        #  - {self.name} -
        # Java: {self.java_version}
        """
    