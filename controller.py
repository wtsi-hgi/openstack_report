
# Route Handlers



# Set up global variables

import utils
from aiohttp import web
import json
from datetime import datetime
import asyncio
from dummy import dummy_cluster_list


from concurrent.futures import ThreadPoolExecutor


time = datetime.now()	
cluster_list = dummy_cluster_list

#Background Job running in separate thread, which updates the global variables time and cluster
async def update_cluster():
	global cluster_list
	cluster_list = utils.load_server_list()
	await utils.load_cpu_time(cluster_list)
	global time 
	time = datetime.now()
	print("Time is now: ", time.strftime("%m/%d/%Y, %H:%M:%S"))
		


main_event_loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor(max_workers=2)
main_event_loop.run_in_executor(executor, utils.run_blocking_tasks, update_cluster)
	


#Handles the overall Get report API
async def get_report(request):
	global time
	global cluster_list
	formated_time = time.strftime("%H:%M:%S, %d-%m-%Y")
	print("Get report called at: ", formated_time)
	response_obj = {'time':formated_time , 'data': cluster_list}
	return web.Response(text=json.dumps(response_obj), headers={'ACCESS-CONTROL-ALLOW-ORIGIN':'*'})

		

# Handles the Get CPU Time API for a particular cluster
# async def get_cpu_time(request):
# 	try:
# 		cpu_hours = 0
# 		user_name_string = request.rel_url.query['user_name']
# 		print("Getting cpu time for: ", user_name_string)
# 		for cluster in cluster_list:
# 			if cluster['user_name'] == user_name_string:
# 				cpu_hours = utils.calculate_cpu_time_for_cluster(cluster)
# 				print("Final: ",cpu_hours)
# 				break
# 		response_obj = {'data': cpu_hours}
# 	except Exception as e:
# 		print("Exception: ", e)
# 		response_obj = {'data': -1}

	# # for server in server_names:
	# return web.Response(text=json.dumps(response_obj), headers={'Access-Control-Allow-Origin':'*'})

# async def refresh_report(request):
# 	time = datetime.now()
# 	print("Refresh state called at: ", time)
# 	cluster_list = utils.load_server_list()
# 	utils.load_cpu_time(cluster_list)
# 	response_obj = {'time':time.strftime("%H:%M:%S, %d-%m-%Y") ,'data': cluster_list}
# 	return web.Response(text=json.dumps(response_obj), headers={'ACCESS-CONTROL-ALLOW-ORIGIN':'*'})
# 	print("Refreshed CLUSTER LIST: ", cluster_list)

