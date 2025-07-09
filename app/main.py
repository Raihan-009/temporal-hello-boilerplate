from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from temporalio import client
import uuid


app = FastAPI()

class NameRequest(BaseModel):
    name: str
class ContainerRequest(BaseModel):
    container_name: str
    image_name: str
    
@app.on_event("startup")
async def startup_event():
    global temporal_client
    temporal_client = await client.Client.connect("temporal:7233")

@app.post("/name")
async def trigger_hello(req: NameRequest):
    try:
        result = await temporal_client.start_workflow(
            "HelloWorkflow",
            req.name,
            id=f"{uuid.uuid4().hex}",
            task_queue="hello-task-queue"
        )
        return {"message": f"Workflow started with run ID: {result.id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/launch-container")
async def launch_container(req: ContainerRequest):
    try:
        result = await temporal_client.start_workflow(
                    "LaunchContainerWorkflow",
                    args=[req.container_name, req.image_name],
                    id=f"launch-container-{req.container_name}",
                    task_queue="hello-task-queue"
                )
        return {"message": f"Workflow started: {result.id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))