#!/bin/bash
# get-elastic-blast.sh: Installs ElasticBLAST in a local virtual environment
#
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Fri 05 Jun 2020 03:41:13 PM EDT

set -u

[[ `hostname -f` =~ 'ncbi.nlm.nih.gov' ]] || {
    echo "Error: this script works only at NCBI";
    exit 1;
}

VENV=${PWD}/.env

[ -d ${VENV} ] || {
    mkdir -p ${VENV};
    python3 -m venv ${VENV};
    source ${VENV}/bin/activate;
    pip install -q elb;
}
#find . -type f -name elastic-blast.py
set -e 
source ${VENV}/bin/activate
command -v elastic-blast.py

echo "To use elastic-blast.py, run the command below to add it to your PATH"
echo "source ${VENV}/bin/activate"
