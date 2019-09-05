#!/bin/bash

source hgi-openrc.sh
echo "Entrypoint running"
exec python test.py
