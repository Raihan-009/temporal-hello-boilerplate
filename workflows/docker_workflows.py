from temporalio import workflow
from datetime import timedelta

@workflow.defn
class LaunchContainerWorkflow:
    @workflow.run
    async def run(self, container_name: str, image_name: str) -> str:
        exists = await workflow.execute_activity(
            "check_container_exists",
            args=[container_name],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        if exists:
            workflow.logger.info("Container with name %s already exists.", container_name)
            return f"Container with name '{container_name}' already exists."

        result = await workflow.execute_activity(
            "launch_docker_container",
            args=[container_name, image_name],
            schedule_to_close_timeout=timedelta(seconds=60),
        )
        workflow.logger.info("[Workflow] : %s container has completed successfully", container_name)
        return result

@workflow.defn
class DestroyContainerWorkflow:
    @workflow.run
    async def run(self, container_name: str) -> str:
        exists = await workflow.execute_activity(
            "check_container_exists",
            args=[container_name],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
        if not exists:
            workflow.logger.info("Container with name %s doesn't exists.", container_name)
            return f"Container with name '{container_name}' doesn't exists."
        result =  await workflow.execute_activity(
            "destroy_docker_container",
            container_name,
            schedule_to_close_timeout=timedelta(seconds=30),
        )
        workflow.logger.info("[Workflow] : %s container has destroyed successfully", container_name)
        return result
