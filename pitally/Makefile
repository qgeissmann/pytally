
all: client  
	python3 setup.py  release sdist

clean:
	rm  -rf dist/*

cleanall:
	make clean -C pitally/server/pitally-client

client:
	make -C pitally/server/pitally-client
