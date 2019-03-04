
all: tarballs

tarballs:
	make clean -C pitally && make -C pitally && cp $(shell ls pitally/dist/*.tar.gz | tail -n 1) dist_tarballs/
	make clean -C pitally_update && make -C pitally_update && cp $(shell ls pitally_update/dist/*.tar.gz| tail -n 1) dist_tarballs/

install:
	make -C dist_tarballs

clean:
	rm -f dist_tarballs/*.tar.gz