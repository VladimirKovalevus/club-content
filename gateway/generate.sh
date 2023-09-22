#!bin/bash

python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m pip install grpcio
python3 -m pip install grpcio-tools

cd ../grpc/
bash build_py.sh
cd ../gateway/