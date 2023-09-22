#!/bin/bash

python3 -m grpc_tools.protoc -I. --python_out=../gateway --grpc_python_out=../gateway grpc.proto