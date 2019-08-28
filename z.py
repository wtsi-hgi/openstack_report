import openstack 
# from osc_lib import utils

# from novaclient.client import Client
# import os


import asyncio
# def get_nova_credentials_v2():
#     d = {}
#     d['version'] = '2'
#     d['username'] = os.environ['OS_USERNAME']
#     d['api_key'] = os.environ['OS_PASSWORD']
#     d['auth_url'] = os.environ['OS_AUTH_URL']
#     d['project_id'] = os.environ['OS_PROJECT_NAME']
#     return d


# credentials = get_nova_credentials_v2();
# nova_client = Client(**credentials)
# servers_list = nova_client.servers.list()


# for s in servers_list:
# 	print(s.diagnostics())
# 	break

from datetime import datetime

import subprocess

import json
import utils


async def test():
	x = await utils.get_cpu_time("eta-hgi-prod-instance-kk8-hail-hail-slave-40")
	print(x)

loop = asyncio.get_event_loop()

# y =  651810000000 + 693640000000 + 713420000000 + 678530000000
# print(y)
asyncio.ensure_future(test())

# connection = openstack.connect()


# for s in connection.compute.servers():
# 	print(s['name'])
# 	bashCommand = "openstack server show {} --diagnostics -f json".format(s['name'])
# 	print(bashCommand)
# 	process = subprocess.Popen(bashCommand.split(), stdout = subprocess.PIPE)
# 	output, error = process.communicate()
# 	if output is not None:
# 		output_json_string = output.decode('utf8').replace("\n", "")
# 		output_dictionary= json.loads(output_json_string)
# 		cpu_time = 0;
# 		print(output_dictionary)
# 		for key, value in output_dictionary.items():
# 			if key.startswith("cpu"):
# 				cpu_time += value		 	
# 		print(cpu_time)
# 	break;

	# print(server['name'])
	
	
	# /servers/id/diagnostics
