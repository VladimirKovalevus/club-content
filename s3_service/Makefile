TAG = golang
UNAME = $(shell uname -s)

ifeq ($(UNAME), Linux)
	INSTALLER = sudo apt install protobuf-compiler
else
	INSTALLER = brew install protobuf
endif

all : build

install :
	$(INSTALLER)

grpc:
	cp ../grpc/grpc.proto .
	cp ../grpc/build_go.sh .
	sh build_go.sh
	rm grpc.proto
	rm build_go.sh
	go mod tidy

build_docker: grpc
	docker build . --tag $(TAG)

run :
	docker run -d -p 8785:8785 $(TAG)
