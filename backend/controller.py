
# Route Handlers



# Set up global variables

import utils
from aiohttp import web
import json
from datetime import datetime
import asyncio
from dummy import dummy_cluster_list



	
#Handles the overall Get report API
async def get_report(request):
	report = request.app['report']
	cluster_list = report.cluster_list
	time = report.time
	formated_time = time.strftime("%H:%M:%S, %d-%m-%Y")
	print("Get report called at: ", formated_time)
	response_obj = {'time':formated_time , 'data': cluster_list}
	return web.Response(text=json.dumps(response_obj), headers={'ACCESS-CONTROL-ALLOW-ORIGIN':'*'})

		
