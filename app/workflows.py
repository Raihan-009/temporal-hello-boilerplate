# app/workflows.py
from datetime import timedelta
from temporalio import workflow
from . import activities         # import the activity module

@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        # execute the activity
        await workflow.execute_activity(
            activities.say_hello,
            name,
            schedule_to_close_timeout=timedelta(seconds=5),
        )
        workflow.logger.info("Workflow finished for %s", name)
        return f"Hello completed for {name}"

