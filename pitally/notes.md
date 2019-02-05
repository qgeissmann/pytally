wget http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip
unzip 2018-11-13-raspbian-stretch-lite.zip
cp 2018-11-13-raspbian-stretch-lite.img pitally_image.img

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
sudo cp ~/repos/pitally-git/pitally/dist/pitally-1.3.0.tar.gz /mnt/loop0p2/home/pi/
sudo cp  /home/quentin/repos/pitally-git/pitally_update/dist/pitally_update-1.0.tar.gz /mnt/loop0p2/home/pi/
sudo systemd-nspawn  --directory /mnt/loop0p2/

# from the chroot:

apt-get update
apt-get upgrade
apt-get install wput tree ipython3 tcpdump nmap ffmpeg python3-pip iputils-ping git

passwd pi # pitally_1234
nano /etc/wpa_supplicant/wpa_supplicant.conf

```
network={
    ssid="pitally"
    psk="pitally_01234"
}
```

raspi-config # ssh +, camera
pip3 install /home/pi/pitally_update-1.0.tar.gz
pip3 install /home/pi/pitally-1.3.0.tar.gz[production]

rm /home/pi/pitally*.tar.gz


/opt/etcher-cli/balena-etcher  -d /dev/mmcblk0 ./ 2018-11-13-raspbian-stretch-lite.zip

pitally_update.sh  --enable-service
pitally.sh  --enable-service

#leave chroot for cleanup

sudo umount -R /dev/loop0p{1,2}
sudo losetup -d /dev/loop0


/opt/etcher-cli/balena-etcher  -d /dev/mmcblk0 ./pitally_image.img


# setup ftp server


* install bftpd
* enable bftpd.socket
* comment out `DENY_LOGIN="Anonymous login disabled."`
#* set `ALLOWCOMMAND_DELE="yes"`

# push to the server
* install wput ffmpeg tree






















#####




#####################################################3
## add 1gb to the image


truncate -s +1G ./image.img
sudo losetup /dev/loop0 ./image.img
sudo fdisk -l /dev/loop0

sudo fdisk /dev/loop0

    p
    d
    2
    n
    p
    2
    98304
    just hit enter to accept the default
    p
    <no>
    w
    q

sudo losetup -d /dev/loop0     # delete the old loop setup
sudo losetup -o $((98304*512)) /dev/loop0 ./image.img
sudo e2fsck -f /dev/loop0
sudo resize2fs /dev/loop0
sudo losetup -d /dev/loop0

dd if=/dev/zero of=/tmp/temp_image bs=1 count=1 seek=1G
cat /tmp/temp_image >> ./2018-11-13-raspbian-stretch-lite.img
rm /tmp/temp_image

fdisk -l  ./2018-11-13-raspbian-stretch-lite.img

# magic number! (first sector of root partition)
sudo losetup --offset $((98304 * 512)) /dev/loop0 ./2018-11-13-raspbian-stretch-lite.img
sudo e2fsck  -f /dev/loop0
sudo resize2fs /dev/loop0
sudo losetup -d /dev/loop0     # delete the old loop setup


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
losd() (
  dev="/dev/loop$1"
  for part in "$dev"?*; do
    if [ "$part" = "${dev}p*" ]; then
      part="${dev}"
    fi
    dst="/mnt/$(basename "$part")"
    sudo umount "$dst"
  done
  sudo losetup -d "$dev"
)

los image.img
sudo umount /dev/loop0p1
sudo mount /dev/loop0p1 /mnt/loop0p2/boot/
cp /usr/bin/qemu-arm-static /mnt/
#losd

sudo cp /usr/bin/qemu-arm-static /mnt/loop0p2/usr/bin/
sudo cp ~/repos/pitally-git/pitally/dist/pitally-1.3.0.tar.gz /mnt/loop0p2/home/pi/
sudo cp  /home/quentin/repos/pitally-git/pitally_update/dist/pitally_update-1.0.tar.gz /mnt/loop0p2/home/pi/
sudo touch /mnt/loop0p1/ssh


#sudo chroot /mnt/loop0p2
cd /mnt/loop0p2

sudo systemd-nspawn --boot

PATH=/bin/:/sbin/:/usr/local/bin/:/usr/local/sbin/:/usr/bin/
# non python deps:
apt-get update
apt-get upgrade
apt-get install wput tree ipython3 tcpdump nmap ffmpeg
enable camera!
passwd pi # pitally_1234

set up connection:

```
network={
    ssid="pitally"
    psk="pitally_01234"
}
```

ntp?


wget update service and pitally
pip3 install both



sudo systemd-nspawn --boot (from without the chroot, in the mount point)
