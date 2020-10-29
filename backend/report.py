#!/usr/bin/env python

"""
A module consisting of utility functions.
"""
from datetime import datetime
from novaclient import client

import asyncio
import dateutil.parser
import json
import openstack
import os
import random
import re
import subprocess
import time as x
import yaml

#Environment Variables from openrc
username = os.getenv('OS_USERNAME')
password = os.getenv('OS_PASSWORD')
auth_url = os.getenv('OS_AUTH_URL')
user_domain_name = os.getenv('OS_USER_DOMAIN_NAME')

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



async def update_report(report):
    """report = {user, server_name, cores, cpu hours, master, slaves. others, tenant, tenant_id}"""

    temp_cluster_list = await load_server_list()
    await load_cpu_time(temp_cluster_list)
    cluster_list = []
    #Function to combine the tenant's together
    def removeList(l):
        for i in l:
            if type(i) == list:
                removeList(i)
            else:
                cluster_list.append(i)
    removeList(temp_cluster_list)
    time = datetime.now()
    print('Time started')
    report.set_time(time)
    report.set_clusters(cluster_list)
    print('Time taken: '.format(datetime.now() - time))

    await asyncio.sleep(1000)


# What if this fails?
async def load_server_list():
    """Load the list of servers and populate it with flavor name, whether the server is a hail master, and other such info"
        # This must use the environmental variables to conenct to keystone.
        Establishes a connection by authenticating with keystone. (blocking)
        Gets all flavours (blocking).
        Creates a dictionary of users.
        Iterates over the list of servers. Each server is mapped to some user and manipulates the user record.
        Creates a dictionary of tenants mapping each 'dictionary of users' to specific tenants
    """

    with open('tenants_conf.yml', 'r') as f:
        tenant_conf = yaml.safe_load(f)
        tenant_names = []
        tenant_ids = []
        for tenant_name in tenant_conf['tenants']:
            tenant_names.append(tenant_name)
            tenant_ids.append(tenant_conf['tenants'][tenant_name])

    stored_tenants = {}
    for project_id in tenant_ids:
        stored_users = {}
        nova = client.Client(version="2", username=username, password=password, project_id=project_id, auth_url=auth_url, user_domain_name=user_domain_name)
    # What if this fails?
        flavor_id_map =  get_flavors(nova)
        for server in nova.servers.list():
            #Reg Ex to determine whether a server is a cluster or not
            cluster_match = re.search("^(?P<user>.+?)-(?P<cluster>.+)-(?P<role>master$|manager(?=-\d{2}$)|worker(?=-\d{2}$))", server.name)
            if cluster_match is not None:
                user = cluster_match.group(1)
                if user == "theta":
                    user = "mercury"
                if cluster_match.group(3) == "master" or cluster_match.group(3) == "manager":
                    is_master = "master"
                else:
                    is_master = "slave"
            else:
                user = "Non-Cluster"
                is_master = "non-cluster"

            flavor_id = server.flavor.get('id')
            vcpus = flavor_id_map.get(flavor_id)
            user_data = stored_users.get(user)
            #Checks user_data and creates/amends a user where necessary
            if user_data is None or user_data['tenant_id'] != project_id:
                user_data = {"user_name": user, "server_names": [server.name], "tenant": tenant_names[tenant_ids.index(project_id)], "tenant_id": project_id}
                user_data['cores'] = vcpus
                user_data['cpu_hours'] = None
                if (is_master == "master"):
                    created_date = server.created
                    user_data['created_date'] = dateutil.parser.parse(created_date).strftime("%d-%m-%Y %H:%M:%S")
                    user_data['slaves'] = 0
                    user_data['master'] = 1
                    user_data['other'] = 0
                elif (is_master == 'slave'):
                    user_data['slaves'] = 1
                    user_data['master'] = 0
                    user_data['other'] = 0
                    created_date = server.created
                    user_data['created_date'] = dateutil.parser.parse(created_date).strftime("%d-%m-%Y %H:%M:%S")
                else:
                    user_data['slaves'] = 0
                    user_data['master'] = 0
                    user_data['other'] = 1
                    created_date = server.created
                    user_data['created_date'] = dateutil.parser.parse(created_date).strftime("%d-%m-%Y %H:%M:%S")
                stored_users[user] = user_data
            else:
                user_data['server_names'].append(server.name)
                user_data['cores'] = user_data['cores'] + vcpus
                if is_master == "slave":
                    user_data['slaves'] = user_data['slaves'] + 1
                elif is_master == "non-cluster":
                    user_data['other'] = user_data['other'] + 1
                else:
                    created_date = server.created
                    user_data['created_date'] = dateutil.parser.parse(created_date).strftime("%d-%m-%Y %H:%M:%S")
                    user_data['master'] = user_data['master'] + 1

        sorted_users = sorted(stored_users.values(), key= lambda x: (x["master"], x["created_date"]),reverse=True)
        stored_tenants[project_id] = sorted_users
    return list(stored_tenants.values())

async def load_cpu_time(tenant_list):
    #calculates the CPU time for each set of clusters (Machines controlled by one user for one tenant)
    for tenant in tenant_list:
        for cluster in tenant:
            try:
                cluster['cpu_hours'] = await calculate_cpu_time_for_cluster(cluster)
            except Exception as e:
                print("Error while loading cpu time for user: ", cluster['user_name'])

#Not functional version of above function - testing parallelisation
'''
async def load_cpu_time(cluster_list):
    for cluster in cluster_list:
        cluster['cpu_hours'] = calculate_cpu_time_for_cluster(cluster)
    try:
        print(asyncio.gather(*[cluster['cpu_hours'] for cluster in cluster_list]))
    except Exception as e:
        print("Error while loading cpu time for user: ", cluster['user_name'])
'''


#Method to get the mapping for the flavors. Mapping = ID : Flavor Name
def get_flavors(nova):
    flavors=nova.flavors.list(detailed=True)
    flavorIdMap = {}

    for flavor in flavors:
        id = flavor.id
        if id is not None:
            flavorIdMap[id] = flavor.vcpus
    print(flavorIdMap)
    return flavorIdMap


async def calculate_cpu_time_for_cluster(cluster):
    cpu_hours = 0
    server_names = cluster['server_names']
    try:
        latest_cpu_hours = await asyncio.gather(*[get_cpu_time(server_name, cluster['tenant_id']) for server_name in server_names])
        cpu_hours = sum(latest_cpu_hours)
    except Exception:
        raise e
    return cpu_hours


#Fetches CPU time from the diagnostics of the instance and caclulates total CPU time usage
async def get_cpu_time(server_name, tenant_id):
    try:
        nova = client.Client(version="2", username=username, password=password, project_id=tenant_id, auth_url=auth_url, user_domain_name=user_domain_name)
        server = nova.servers.list(search_opts={'name': server_name})
        if server is not None:
            process = server[0].diagnostics()
            output = process[1]
            print("=-=-=-=-=- Diagnostics for " + server_name + " -=-=-=-=-=")
            print(output)
            cpu_time = 0 
            for key, value in output.items():
                if key.startswith("cpu"):
                    print(key, ":", value)
                    cpu_time += value
            print(cpu_time)
            return round(cpu_time/(3600*1000000000))
    except Exception as e:
        print("Could not calculate cputime for:", server_names)
        raise e
