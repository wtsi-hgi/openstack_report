#!/usr/b

import utils
from aiohttp import web
import json



async def handle(request):
	data = utils.get_master_list()
	response_obj = {'status': 'success', 'data': data}
	return web.Response(text=json.dumps(response_obj))

app = web.Application()

app.router.add_get('/report', handle)

web.run_app(app)


