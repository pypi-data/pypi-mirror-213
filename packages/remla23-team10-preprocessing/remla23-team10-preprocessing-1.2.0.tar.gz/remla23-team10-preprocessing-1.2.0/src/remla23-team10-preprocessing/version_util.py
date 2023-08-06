from importlib import metadata

class VersionUtil:
    @classmethod
    def get_version(cls):
        try:
            return metadata.version('remla23-team10-preprocessing')
        except metadata.PackageNotFoundError:
            return 'Package not found'