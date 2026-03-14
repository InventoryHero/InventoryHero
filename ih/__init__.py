import importlib.metadata

# TODO IMPLEMENT THIS USING IMPORTLIB.METADATA.VERSION
try:
    __version__ = importlib.metadata.version(__package__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "dev"
