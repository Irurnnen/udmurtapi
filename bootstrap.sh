#!/usr/bash

if [ -e ./data/init.complete ]
then
    echo "INFO:     The DB has already been init"
    uvicorn app.main:app --host 0.0.0.0 --port 2180
else
    python3 bootstrap.py
    exit_status=$?
    if [ $exit_status -ne 0 ]
    then
        echo "ERROR WHILE bootstrap.py with code ${exit_status}"
    else
        echo "INFO:     Init complete successfully"
        uvicorn app.main:app --host 0.0.0.0 --port 2180
    fi
fi