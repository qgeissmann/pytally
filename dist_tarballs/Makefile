PITALLY_TB:=$(shell ls pitally-*.tar.gz | tail -n 1)
PITALLY_UPD_TB:=$(shell ls pitally_update-*.tar.gz | tail -n 1)

install:
	pip3 install scapy
	pip3 install $(PITALLY_UPD_TB)
	pip3 install $(PITALLY_TB).["server","hardware","utils"]

