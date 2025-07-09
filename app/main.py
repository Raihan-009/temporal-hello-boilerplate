from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from temporalio import client
from workflows.workflows import HelloWorkflow
import uuid

app = FastAPI()

class NameRequest(BaseModel):
    name: str

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
