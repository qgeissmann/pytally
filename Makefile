
tarballs:
	make -C pitally && cp pitally/dist/*.tar.gz dist_tarballs/
	make -C pitally_update && cp pitally_update/dist/*.tar.gz dist_tarballs/

install: tarballs
	make -C dist_tarballs