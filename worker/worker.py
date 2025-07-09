import asyncio
import logging
import os
from temporalio import client, worker
from workflows.workflows import HelloWorkflow
from workflows.docker_workflows import LaunchContainerWorkflow
from activities.activities import say_hello
from activities.docker_activities import check_container_exists, launch_docker_container

logging.basicConfig(level=logging.INFO)

async def main():
    
    temporal_address = os.getenv("TEMPORAL_SERVER_ADDRESS")
    namespace = os.getenv("TEMPORAL_NAMESPACE")
    task_queue = os.getenv("TASK_QUEUE")

    conn = await client.Client.connect(temporal_address, namespace=namespace)

    async with worker.Worker(
        conn,
        task_queue=task_queue,
        workflows=[HelloWorkflow, LaunchContainerWorkflow],
        activities=[say_hello, check_container_exists, launch_docker_container],
    ):
        logging.info("Worker is running and polling task queue...")
        await asyncio.Event().wait()  # Keeps the worker alive

if __name__ == "__main__":
    asyncio.run(main())
