# generate a dist
python3 setup.py  release sdist

# on the sever
`sudo pip3 install pitally-1.0.tar.gz`
`sudo pitally.sh  --enable-service`