
import asyncio

# Runs in a separate thread. On every iteration, it runs the couroutine in a blocking way. There is no event loop. To Answer: What if the coroutine fails? Do coroutines return an exception? 
def run_blocking_tasks(coroutine, *args):
    while True: 
        coroutine_object = coroutine(*args) #Example: update_report(report)
        asyncio.run(coroutine_object)
    
