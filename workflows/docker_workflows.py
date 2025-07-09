from temporalio import workflow
from datetime import timedelta

@workflow.defn
class LaunchContainerWorkflow:
    @workflow.run
    async def run(self, container_name: str, image_name: str) -> str:
        exists = await workflow.execute_activity(
            "check_container_exists",  # Use activity name as string
            args=[container_name],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        if exists:
            workflow.logger.info("Container with name %s already exists.", container_name)
            return f"Container with name '{container_name}' already exists."

        result = await workflow.execute_activity(
            "launch_docker_container",  # Use activity name as string
            args=[container_name, image_name],
            schedule_to_close_timeout=timedelta(seconds=15),
        )
        workflow.logger.info("Workflow finished for %s container", container_name)
        return result
