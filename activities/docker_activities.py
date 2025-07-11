import docker
from temporalio import activity

def get_docker_client():
    return docker.from_env()

@activity.defn(name="check_container_exists")
async def check_container_exists(container_name: str) -> bool:
    client = get_docker_client()
    try:
        container = client.containers.get(container_name)
        return True
    except docker.errors.NotFound:
        return False

@activity.defn(name="launch_docker_container")
async def launch_docker_container(container_name: str, image_name: str) -> str:
    client = get_docker_client()
    container = client.containers.run(
        image=image_name,
        name=container_name,
        detach=True
    )
    return f"Container '{container.name}' launched with image '{image_name}'"

@activity.defn(name="destroy_docker_container")
async def destroy_docker_container(container_name: str) -> str:
    client = get_docker_client()
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return f"Container '{container_name}' destroyed successfully."
    except docker.errors.NotFound:
        raise Exception(f"Container '{container_name}' not found.")
    except Exception as e:
        raise Exception(f"Failed to destroy container '{container_name}': {e}")
