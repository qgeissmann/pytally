# generate a dist
python3 setup.py  release sdist

# on the sever
`sudo pip install dist/pitally-1.0.tar.gz`
`sudo pitally.sh  --enable-service`