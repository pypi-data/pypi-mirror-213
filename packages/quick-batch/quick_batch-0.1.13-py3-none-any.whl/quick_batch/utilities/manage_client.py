import docker
from utilities import log_exceptions


# create client for docker
@log_exceptions
def create_client():
    return docker.from_env()
