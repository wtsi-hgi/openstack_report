# <ins>__HGI-Openstack-Cluster-Report__</ins>

This project allows for analysis of HGI tenants. The project is dockerized and sectioned into two halves: The backend, and the Frontend. As such, this will be a guide on setting up each half.


## <ins>__Guide__</ins>

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
 * Clone the repository
 * Navigate to backend/
 * Install requirements and ensure secret files are in the directory
 * Run ```bash entrypoint.sh```
 * If setup correctly, entrypoint.sh should run app.py and the backend should begin to output terminal diagnostics

#### Launching the app:
 * Once running, the backend of the app can be found at **<localhost:3000/api/report>**

 
### <ins>The Frontend:</ins>
