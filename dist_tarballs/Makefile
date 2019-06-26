PITALLY_TB:=$(shell ls pitally-*.tar.gz | tail -n 1)
PITALLY_UPD_TB:=$(shell ls pitally_update-*.tar.gz | tail -n 1)

install:
	pip install $(PITALLY_UPD_TB)
	pip install $(PITALLY_TB)["server","hardware","production"]

