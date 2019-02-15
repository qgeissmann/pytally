
tarballs:
	make -C pitally && cp $(shell ls pitally/dist/*.tar.gz | tail -n 1) dist_tarballs/
	make -C pitally_update && cp $(shell ls pitally_update/dist/*.tar.gz| tail -n 1) dist_tarballs/

install:
	make -C dist_tarballs