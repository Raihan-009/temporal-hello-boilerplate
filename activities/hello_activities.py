from temporalio import activity

@activity.defn(name="say_hello")
async def say_hello(name: str):
    return f"Hello {name}!"
