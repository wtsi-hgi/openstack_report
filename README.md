# HGI-Openstack-Cluster-Report

This project allows for analysis of HGI tenants. The project is dockerized and sectioned into two halves: The backend, and the Frontend. As such, this will be a guide on setting up each half.


             # Guide

## The Backend
The backend collates a dictionary of instance data roughly every 15 minutes; it grabs information about the Number of Nodes, Number of Cores, Number of CPU hours and groups this per user per tenant.

### Requirements
 * Python 3.7
 * Python3-pip
 * Ensure the requirements in backend/requirements.txt are installed (ran in backend/entrypoint.sh)
 * Appropriate Secret files in the directory
     * hgi-openrc.sh
     * tenants_conf.yml
