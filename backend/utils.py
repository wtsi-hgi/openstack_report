#!/usr/bin/env python

"""
A module consisting of utility functions. 
"""
import openstack 
import time
import random
import os
# from credentials import get_keystone_creds

# creds = get_keystone_creds()


# novaclient.Client(Version, User, Password, Project_ID, Auth_URL, region_name='Region1')

import subprocess
import json
import asyncio 


from datetime import datetime
import dateutil.parser


def get_flavors(connection):

	
	flavors = connection.list_flavors(connection)
	flavorIdMap = {}
	for flavor in flavors:
		id = flavor.get('id', None)
		if id is not None:
			flavorIdMap[id] = flavor.get('vcpus', None)
	print(flavorIdMap)
	return flavorIdMap
		
async def get_cpu_time(server_name):
	try:
		bashCommand = "openstack server show {} --diagnostics -f json".format(server_name)
		print(bashCommand)
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		output, error = process.communicate()
		print("ërror ", error)
		print("output ", output)
		if output is not None:
			output_json_string = output.decode('utf8').replace("\n", "")
			output_dictionary= json.loads(output_json_string)
			cpu_time = 0;
		
			for key, value in output_dictionary.items():
				if key.startswith("cpu"):
					print(key, ":" , value) 
					cpu_time += value
			return round(cpu_time/(3600*1000000000))
	except Exception as e:
		print("Could not calculate cputime for:", server_names)
		raise e				

async def calculate_cpu_time_for_cluster(cluster):
	cpu_hours = 0
	server_names = cluster['server_names']
	try:
		for server_name in server_names:
			latest_cpu_hours = await get_cpu_time(server_name)
			cpu_hours = latest_cpu_hours + cpu_hours
	except Exception:
		raise e
	return cpu_hours


# cluster_list has one row per user
async def load_cpu_time(cluster_list):
	for cluster in cluster_list:
		try:
			cluster['cpu_hours'] = await calculate_cpu_time_for_cluster(cluster)
		except Exception as e:
			print("Error while loading cpu time for user: ", cluster['user_name'])

# async def load_cpu_time_dummy(cluster_list):
# 	for cluster in cluster_list:
# 		await asyncio.sleep(1)
# 		cluster['cpu_hours'] = random.randint(1,100)



# What if this fails?
async def load_server_list():
	"""Load the list of servers and populate it with flavor name, whether the server is a hail master, and other such info"
		# This must use the environmental variables to conenct to keystone.
		Establishes a connection by authenticating with keystone. (blocking)
		Gets all flavours (blocking).
		Creates a dictionary of users.
		Iterates over the list of servers. Each server is mapped to some user and manipulates the user record. 

	"""
 

	connection = openstack.connect()
	# What if this fails?
	flavor_id_map =  get_flavors(connection)
	stored_users = {}
	for server in connection.compute.servers():
		user = server.get('metadata', {}).get('deployment_owner', None)
		flavour_id = server.get('flavor', {}).get('id')
		vcpus = flavor_id_map.get(flavour_id)
		is_master = server.get('metadata', {}).get('role_name', None) == 'hail-master'
		user_data = stored_users.get(user)
		if user_data is None:
			user_data = {"user_name": user, "server_names": [server['name']]}
			user_data['cores'] = vcpus
			user_data['cpu_hours'] = None
			if (is_master):
				created_date = server.get('created_at', None)
				user_data['created_date'] = datetime.strptime(created_date, '%Y-%m-%dT%H:%M:%S%Z').strftime("%d-%m-%Y %H:%M%S")
				user_data['slaves'] = 0
				user_data['master'] = 1
			else:
				user_data['slaves'] = 1	
				user_data['master'] = 0
				created_date = server.get('created_at', None)
				# user_data['created_date'] = datetime.strptime(created_date, '%Y-%m-%dT%H:%M:%S%Z').strftime("%d-%m-%Y %H:%M:%S")
				user_data['created_date'] = dateutil.parser.parse(created_date).strftime("%d-%m-%Y %H:%M:%S")
			stored_users[user] = user_data
		else:
			user_data['server_names'].append(server['name'])
			user_data['cores'] = user_data['cores'] + vcpus
			if not is_master:
				user_data['slaves'] = user_data['slaves'] + 1
			else:
				created_date = server.get('created_at', None)
				# user_data['created_date'] = datetime.strptime(created_date, '%Y-%m-%dT%H:%M:%S%z').strftime("%d-%m-%Y %H:%M:%S")
				user_data['created_date'] = dateutil.parser.parse(created_date).strftime("%d-%m-%Y %H:%M:%S")
				user_data['master'] = user_data['master'] + 1

	d = sorted(stored_users.values(), key= lambda x: (x["master"], x["created_date"]),reverse=True)
	print (d)
	return d




#Report class with the following functions: 
class Report:
	'''This class describes a report'''

	def __init__(self, time, cluster_list):
		self.time = time
		self.cluster_list = cluster_list

	def set_time(self, new_time):
		self.time = new_time

	def set_clusters(self,new_clusters):
		self.cluster_list = new_clusters


# Runs in a separate thread. On every iteration, it starts a new event loop, schedules a couroutine on it, and then closes the loop. To Answer: What if the coroutine fails? Do coroutines return an exception? 
def run_blocking_tasks(coroutine, *args):
	while True:	
		coroutine_object = coroutine(*args) #Example: update_report(report)
		asyncio.run(coroutine_object)
	


async def update_report(report):
	"""report = {user, server_name, cores, cpu hours, master, slaves}
	

	"""
	temp_cluster_list = await load_server_list()
	await load_cpu_time(temp_cluster_list)
	time = datetime.now()
	report.set_time(time)
	report.set_clusters(temp_cluster_list)
	await asyncio.sleep(1000)
	
	





