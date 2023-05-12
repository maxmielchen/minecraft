import os

class BaseEnvironments:
    release_tag = os.getenv("RELEASE_TAG")
    repository = os.getenv("REPOSITORY")
    registry = os.getenv("REGISTRY")

    def get_release_tag(self):
        return self.release_tag
    
    def get_repository(self):
        return self.repository
    
    def get_registry(self):
        return self.registry

