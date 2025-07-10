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
class ContainerNameRequest(BaseModel):
    container_name: str
    
@app.on_event("startup")
async def startup_event():
    global temporal_client
    temporal_client = await client.Client.connect("temporal:7233")

@app.post("/hello")
async def trigger_hello(req: NameRequest):
    try:
        result = await temporal_client.start_workflow(
            "HelloWorkflow",
            req.name,
            id=f"printing-name-{(req.name).lower()}",
            task_queue="central-task-queue"
        )
        return {"message": f"Workflow started with run ID: {result.id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/launch")
async def launch_container(req: ContainerRequest):
    try:
        result = await temporal_client.start_workflow(
                    "LaunchContainerWorkflow",
                    args=[req.container_name, req.image_name],
                    id=f"launch-container-{req.container_name}",
                    task_queue="central-task-queue"
                )
        return {"message": f"Workflow started with run ID: {result.id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/destroy")
async def destroy_container(req: ContainerNameRequest):
    try:
        result = await temporal_client.start_workflow(
            "DestroyContainerWorkflow",
            args=[req.container_name],
            id=f"destroy-container-{req.container_name}",
            task_queue="central-task-queue",
        )
        return {"message": f"Workflow started with run ID: {result.id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))