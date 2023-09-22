UNAME = $(shell uname -s)

ifeq ($(UNAME), Linux)
	CMD = .
else
	CMD = source
endif


all : build

build :
	touch app.log
	bash generate.sh

run : build
	$(CMD) venv/bin/activate && bash build_py.sh && uvicorn main:app --reload --port 9999

docker :
	bash build_py.sh
	docker build .

open :
	open http://127.0.0.1:9999/docs

clean :
	rm -rf venv __pycache__
	rm -rf app.log