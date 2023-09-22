#!/bin/bash

protoc --go-grpc_out=../s3_service --go_out=../s3_service grpc.proto