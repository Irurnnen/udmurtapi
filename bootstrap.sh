#!/usr/bash

py bootstrap.py
exit_status=$?
if [ $? -ne 0 ];
then
    echo "ERROR WHILE bootstrap.py with code ${exit_status}"
fi
echo "INFO: "