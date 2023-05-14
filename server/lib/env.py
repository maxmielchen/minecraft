import os

class BaseEnvironments:
    "Environment variable holder that finds out information about the 'GitHub Action Runner'"
    release_tag = os.getenv("RELEASE_TAG")
    repository = os.getenv("REPOSITORY")
    registry = os.getenv("REGISTRY")

    def get_release_tag(self):
        "Returns the release tag to be used, such as 'v0.1.9'"
        return self.release_tag
    
    def get_repository(self):
        "Returns the repository running this script, such as 'maxmielchen/minecraft'"
        return self.repository
    
    def get_registry(self):
        "Returns the registry running this script, such as 'ghcr.io' or 'hub.docker.com'"
        return self.registry
    