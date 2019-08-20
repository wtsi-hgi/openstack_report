#!/usr/bin/env python

import openstack 
# from credentials import get_keystone_creds

# creds = get_keystone_creds()


# novaclient.Client(Version, User, Password, Project_ID, Auth_URL, region_name='Region1')



def get_master_list():
	connection = openstack.connect()
	servers = connection.list_servers()
	data = []
	for server in servers:
		metadata = server['metadata']
		user = metadata.get('deployment_owner', "Not Found")
		isMaster = metadata.get('role_name', "Not Found") == 'hail-master'
		updated = server['updated']
		created = server['created']
		row = {"user": user,
			"updated_time":updated,
			"created_time": created}
		if (isMaster):
			data.append(row)
	return data
			





	