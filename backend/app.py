#!/usr/b

import asyncio 
from aiohttp import web
from concurrent.futures import ThreadPoolExecutor
from utils import Report, run_blocking_tasks, update_report
from datetime import datetime
from routes import load_routes
from dummy import dummy_cluster_list

if __name__ == '__main__':

	# Initialize report data which will persist and be modified during the lifetime of the app. 
	app = web.Application()
	app['report'] = Report(datetime.now(), dummy_cluster_list)

	# Run Background jobs in parallel thread
	main_event_loop = asyncio.get_event_loop()
	executor = ThreadPoolExecutor(max_workers=1)
	main_event_loop.run_in_executor(executor, run_blocking_tasks, update_report, app['report'])

	# Routes 
	load_routes(app)
	web.run_app(app, port = 3000)




