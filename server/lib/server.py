
class Server:
    "Holds information from a minecraft server"

    def __init__(self, server: str, version: str, source: str, java_version: int):
        self.server: str = server
        self.version: str = version
        self.source: str = source
        self.java_version: int = java_version

    def get_server(self) -> str:
        "Returns server name eg paper, bukkit, spigot, vanilla"
        return self.server
    
    def get_version(self) -> str:
        "Returns the version of the server"
        return self.version
    
    def get_source(self) -> str:
        "Returns the location of the source"
        return self.source
    
    def get_java_version(self) -> int:
        "Specifies the minimum supported java version"
        return self.java_version
    
    def info(self) -> str:
        "Returns an info record"
        return f"""
        #  - {self.server} -
        # Version: {self.version}
        """
