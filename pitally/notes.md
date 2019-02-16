
wget http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip
unzip 2018-11-13-raspbian-stretch-lite.zip
cp 2018-11-13-raspbian-stretch-lite.img pitally_image.img

PITALLY_TARBALL=pitally-1.3.2.tar.gz
PITALLY_UPDATE_TARBALL=pitally_update-1.0.1.tar.gz

# mount the image in a loop
los() (
  img="$1"
  dev="$(sudo losetup --show -f -P "$img")"
  echo "$dev"
  for part in "$dev"?*; do
    if [ "$part" = "${dev}p*" ]; then
      part="${dev}"
    fi
    dst="/mnt/$(basename "$part")"
    echo "$dst"
    sudo mkdir -p "$dst"
    sudo mount "$part" "$dst"
  done
)

los pitally_image.img
sudo mount /dev/loop0p1 /mnt/loop0p2/boot

sudo cp /usr/bin/qemu-arm-static /mnt/loop0p2/usr/bin/
sudo cp ~/repos/pitally-git/pitally/dist/$PITALLY_TARBALL /mnt/loop0p2/home/pi/
sudo cp  ~/repos/pitally-git/pitally_update/dist/$PITALLY_UPDATE_TARBALL /mnt/loop0p2/home/pi/
sudo systemd-nspawn  --directory /mnt/loop0p2/

# from the chroot:

apt-get update
apt-get upgrade
apt-get install wput tree ipython3 tcpdump nmap ffmpeg python3-pip iputils-ping git
##
passwd pi # pitally_1234
nano /etc/wpa_supplicant/wpa_supplicant.conf

```
network={
    ssid="pitally"
    psk="pitally_01234"
}
```

raspi-config # ssh +, camera
pip3 install /home/pi/$PITALLY_UPDATE_TARBALL
pip3 install /home/pi/$PITALLY_TARBALL[production]

rm /home/pi/pitally*.tar.gz


/opt/etcher-cli/balena-etcher  -d /dev/mmcblk0 ./ 2018-11-13-raspbian-stretch-lite.zip

pitally_update.sh  --enable-service
pitally.sh  --enable-service

#leave chroot for cleanup

sudo umount -R /dev/loop0p{1,2}
    sudo losetup -d /dev/loop0


/opt/etcher-cli/balena-etcher  -d /dev/mmcblk0 ./pitally_image.img


# setup ftp server

yaourt -S pure-ftpd tree ffmpeg


pure-pw useradd pi -u ftp -d /srv/ftp # pitally_01234
#pure-pw passwd pi
pure-pw mkdb
echo "/bin/false" >> /etc/shells

# We disable the anonymous account.
ChrootEveryone               no
NoAnonymous                  no
PureDB                       /etc/pureftpd.pdb
AnonymousCantUpload          yes
CreateHomeDir                yes
KeepAllFiles                 yes
MinUID                       14
AntiWarez                    no
NoTruncate                   yes
TLS                          0



sudo systemctl enable pure-ftpd.service
#test :
dd if=/dev/zero of=/tmp/test_ftp count=1024 bs=1024
wput /tmp/test_ftp  ftp://pi:pitally_01234@localhost
curl ftp://localhost/tmp/test_ftp > /dev/null

#router

uci set system.@system[0].hostname='pitally-router'
uci commit system
/etc/init.d/system reload



for i in $(seq 1 9); do dd if=/dev/zero of=./test_ftp$i.mp4 count=100024 bs=1024; done
dd if=/dev/zero of=./test_ftp$i.h264 count=100024 bs=1024

lftp -c "open -u pi,pitally_01234 pitally-drive;mirror -R /tmp/test_ftp_dir  /tmp/test_ftp_dir --Remove-source-files --include-glob='*.mp4' -c"
