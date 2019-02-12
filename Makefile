
all:
    make -C pitally && cp pitally/dist/*.tar.gz dist/
    make -C pitally_update && cp pitally_update/dist/*.tar.gz dist/