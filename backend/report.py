#!/usr/bin/env python

"""
A module consisting of utility functions.
"""
from novaclient import client
import openstack
import os
import time as x
import random
import re
# from credentials import get_keystone_creds
# creds = get_keystone_creds()
# novaclient.Client(Version, User, Password, Project_ID, Auth_URL, region_name='Region1')

import subprocess
import json
import asyncio


from datetime import datetime
import dateutil.parser

#Nova Environment variables
version = "2"
username = os.getenv('OS_USERNAME')
password = os.getenv('OS_PASSWORD')
project_id = os.getenv('OS_PROJECT_ID')
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
    """report = {user, server_name, cores, cpu hours, master, slaves}
    """

    temp_cluster_list = await load_server_list()
    await load_cpu_time(temp_cluster_list)
    time = datetime.now()
    print('Time started')
    report.set_time(time)
    report.set_clusters(temp_cluster_list)

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
    """

    nova = client.Client(version=version, username=username, password=password, project_id=project_id, auth_url=auth_url, user_domain_name=user_domain_name)
    # What if this fails?
    flavor_id_map =  get_flavors(nova)
    stored_users = {}
    for server in nova.servers.list():
        cluster_match = re.search("^(?P<user>.+?)-(?P<cluster>.+)-(?P<role>master$|manager(?=-\d{2}$)|worker(?=-\d{2}$))", server.name)
        if cluster_match is not None:
            user = cluster_match.group(1)
            if user == "theta" and "mercury" in server.name:
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
        if user_data is None:
            user_data = {"user_name": user, "server_names": [server.name]}
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

    d = sorted(stored_users.values(), key= lambda x: (x["master"], x["created_date"]),reverse=True)
    print (d)
    return d

async def load_cpu_time(cluster_list):
    for cluster in cluster_list:
        try:
            cluster['cpu_hours'] = await calculate_cpu_time_for_cluster(cluster)
        except Exception as e:
            print("Error while loading cpu time for user: ", cluster['user_name'])

'''
async def load_cpu_time(cluster_list):
    for cluster in cluster_list:
        cluster['cpu_hours'] = calculate_cpu_time_for_cluster(cluster)
    try:
        asyncio.gather(*[cluster['cpu_hours'] for cluster in cluster_list])
    except Exception as e:
        print("Error while loading cpu time for user: ", cluster['user_name'])
'''


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
        latest_cpu_hours = await asyncio.gather(*[get_cpu_time(server_name) for server_name in server_names])
        cpu_hours = sum(latest_cpu_hours)
    except Exception:
        raise e
    return cpu_hours


# cluster_list has one row per user

async def get_cpu_time(server_name):
    try:
        nova = client.Client(version=version, username=username, password=password, project_id=project_id, auth_url=auth_url, user_domain_name=user_domain_name)
        server = nova.servers.list(search_opts={'name': server_name})
        if server is not None:
            process = server[0].diagnostics()
            output = process[1]
            print("--Diagnostics for " + server.name + "--")
            print(output)
            cpu_time = 0
            for key, value in output.items():
                if key.startswith("cpu"):
                    print(key, ":", value)
                    cpu_time += value
            return round(cpu_time/(3600*1000000000))
    except Exception as e:
        print("Could not calculate cputime for:", server_names)
        raise e
