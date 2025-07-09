from temporalio import activity

@activity.defn
async def say_hello(name: str) -> str:
    print(f"[Activity] Hello {name}")
