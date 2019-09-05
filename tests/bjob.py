import subprocess
import json


async def get_cpu_time(server_name):
	
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
		return round(cpu_time)


