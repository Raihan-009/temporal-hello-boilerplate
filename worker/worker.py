import asyncio
import logging
import os
from temporalio import client, worker
from workflows.workflows import HelloWorkflow
from activities.activities import say_hello

logging.basicConfig(level=logging.INFO)

async def main():
    
    temporal_address = os.getenv("TEMPORAL_SERVER_ADDRESS")
    namespace = os.getenv("TEMPORAL_NAMESPACE")
    task_queue = os.getenv("TASK_QUEUE")

    conn = await client.Client.connect(temporal_address, namespace=namespace)

    async with worker.Worker(
        conn,
        task_queue=task_queue,
        workflows=[HelloWorkflow],
        activities=[say_hello],
    ):
        logging.info("Worker is running and polling task queue...")
        await asyncio.Event().wait()  # Keeps the worker alive

if __name__ == "__main__":
    asyncio.run(main())
