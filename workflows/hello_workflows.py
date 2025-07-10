from datetime import timedelta
from temporalio import workflow
from activities.hello_activities import say_hello

@workflow.defn
class HelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        await workflow.execute_activity(
            say_hello,
            name,
            schedule_to_close_timeout=timedelta(seconds=5),
        )
        workflow.logger.info("Workflow finished for %s", name)
        return f"Hello task completed for {name}"

