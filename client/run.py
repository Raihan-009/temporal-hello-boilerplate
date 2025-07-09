import asyncio
import sys
from temporalio import client
import uuid

async def main(name: str) -> None:
    # Connect to Temporal server
    c = await client.Client.connect("localhost:7233")

    # Start the HelloWorkflow with the given name
    handle = await c.start_workflow(
        "HelloWorkflow",
        name,                                                   # Argument to the workflow
        id=f"hello-{name.lower()}-{uuid.uuid4().hex}",          # Unique workflow ID
        task_queue="hello-task-queue",                          # Queue that worker listens to
    )

    print(f"Started workflow with ID: {handle.id}")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "World"
    asyncio.run(main(name))
