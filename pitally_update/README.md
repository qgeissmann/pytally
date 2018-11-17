# generate a dist
```
python3 setup.py  release sdist
```

# on the sever
```
sudo pip3 install --ignore-installed pitally_update-1.0.tar.gz
sudo pitally_update.sh  --enable-service
```
