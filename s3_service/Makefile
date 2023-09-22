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

build :
	bash build_go.sh
	docker build . --tag $(TAG)

run :
	docker run -d -p 8785:8785 $(TAG)
