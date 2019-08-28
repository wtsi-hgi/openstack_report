#!/usr/b

import utils
from aiohttp import web

import asyncio 
import routes



if __name__ == '__main__':
	app = web.Application()

	# Routes 
	routes.load_routes(app)
	

	web.run_app(app, port = 8082)




