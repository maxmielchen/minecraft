
class Server:

    def __init__(self, server: str, version: str, source: str, java_version: int):
        self.server: str = server
        self.version: str = version
        self.source: str = source
        self.java_version: int = java_version

    def get_server(self) -> str:
        return self.server
    
    def get_version(self) -> str:
        return self.version
    
    def get_source(self) -> str:
        return self.source
    
    def get_java_version(self) -> int:
        return self.java_version
    
    def info(self) -> str:
        return f"""
        #  - {self.server} -
        # Version: {self.version}
        """
