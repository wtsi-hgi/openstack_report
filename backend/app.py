#!/usr/bin/python

import asyncio 
from aiohttp import web
from concurrent.futures import ThreadPoolExecutor
from report import Report, update_report
from utils import run_blocking_tasks
from datetime import datetime
from routes import load_routes
from dummy import dummy_cluster_list
import logging


async def run_background_tasks(app):
	app['report'] = Report(datetime.now(), dummy_cluster_list)
	loop = asyncio.get_event_loop()
	executor = ThreadPoolExecutor(max_workers=1)
	loop.run_in_executor(executor, run_blocking_tasks, update_report, app['report'])



if __name__ == '__main__':

	# Initialize report data which will persist and be modified during the lifetime of the app. 
	app = web.Application()

	# Run Background jobs in parallel thread
	app.on_startup.append(run_background_tasks)
	# Routes 
	load_routes(app)
	web.run_app(app, port = 3000)




