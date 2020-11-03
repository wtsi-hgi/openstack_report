# <ins>__HGI-Openstack-Cluster-Report__</ins>

This project allows for analysis of HGI tenants. The project is dockerized and sectioned into two halves: The backend, and the Frontend. As such, this will be a guide on setting up each half.


## <ins>__Guide:__</ins>

### <ins>The Backend:</ins>
The backend collates a dictionary of instance data roughly every 15 minutes; it grabs information about the Number of Nodes, Number of Cores, Number of CPU hours and groups this per user per tenant.

#### Requirements:
 * Python 3.7
 * Python3-pip
 * Other requirements are contained in: backend/requirements.txt
 * Appropriate Secret files in the directory
     * hgi-openrc.sh
     * tenants_conf.yml

#### Setup:
`Note: Following the steps from the DockerFile will give you the necessary steps for setup`
 * Clone the repository
 * Navigate to backend/
 * Install requirements and ensure secret files are in the directory
 * Run ```bash entrypoint.sh```
 * If setup correctly, entrypoint.sh should run app.py and the backend should begin to output terminal diagnostics

#### Launching the app:
 * Once running, the backend of the app can be found at **<localhost:3000/api/report>**


### <ins>The Frontend:</ins>
The frontend of the app is ran on vue.js via Node. Running the frontend without the backend brings up the blank page with with only the header. If the backend is up, this populates a table with the same fields as those from the backend.

#### Requirements:
 * Node v10
 * Other requirements are found in package*.json files

#### Setup:
`Note: Following the steps from the DockerFile will give you the necessary steps for setup`
 * Install Node v10
 * Run npm install
 * If running locally and not in development mode, the .env.development will need to be pointed at the IP Address of the backend
 * Run npm run serve

#### Launching the app:
 * Once running, the frontend of the app can be found at **<localhost:8080/cluster-report>**
