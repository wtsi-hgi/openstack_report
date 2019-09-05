
from bjob import get_cpu_time
import asyncio




async def init():
	server_name = "eta-hgi-prod-instance-kk8-hail-hail-master-01"
	x = await get_cpu_time(server_name)
	print(x)

loop = asyncio.get_event_loop()
loop.run_until_complete(init())


