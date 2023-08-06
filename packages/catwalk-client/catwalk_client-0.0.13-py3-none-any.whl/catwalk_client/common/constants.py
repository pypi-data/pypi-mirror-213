from importlib import metadata

CATWALK_CLIENT_VERSION = metadata.version("catwalk_client")

CATWALK_AUTH_HEADER = "Catwalk-Authorization"
CATWALK_CLIENT_LOCATION = "Client-Location"
CATWALK_USER_AGENT_HEADER_VALUE = f"Catwalk-Client/{CATWALK_CLIENT_VERSION}"
CATWALK_CLIENT_THREAD_NAME_PREFIX = "catwalk_client_"
