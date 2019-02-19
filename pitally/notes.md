
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

#Install pitally

# setup pureftpd
yaourt -S pure-ftpd tree ffmpeg


pure-pw useradd pi -u ftp -d /srv/ftp # pitally_01234
#pure-pw passwd pi
pure-pw mkdb
echo "/bin/false" >> /etc/shells

echo "
ChrootEveryone               no
BrokenClientsCompatibility   no
MaxClientsNumber             50
Daemonize                    yes
ChrootEveryone               no
BrokenClientsCompatibility   no
MaxClientsNumber             50
Daemonize                    yes
MaxClientsPerIP              8
VerboseLog                   no
DisplayDotFiles              yes
AnonymousOnly                no
NoAnonymous                 no
SyslogFacility none
FortunesFile /etc/pure-ftpd/welcome.msg
DontResolve                  yes
MaxIdleTime                  15
PureDB                       /etc/pureftpd.pdb
LimitRecursion               10000 8
AnonymousCanCreateDirs       no
MaxLoad                      4
AntiWarez                    no
Umask                        133:022
MinUID                       14
AllowUserFXP                 no
AllowAnonymousFXP            no
ProhibitDotFilesWrite        no
ProhibitDotFilesRead         no
AutoRename                   no
AnonymousCantUpload          yes
AltLog clf:/var/log/pureftpd.log
KeepAllFiles                 yes
CreateHomeDir                yes
MaxDiskUsage                   99
CustomerProof                yes
NoTruncate                   yes
TLS 0
TLSCipherSuite -S:HIGH:MEDIUM:+TLSv1
" > /etc/pure-ftpd/pure-ftpd.conf

sudo chown ftp:ftp /srv/ftp
sudo systemctl enable pure-ftpd.service
sudo pitally_drive.sh --enable-service


#test :
dd if=/dev/zero of=/tmp/test_ftp count=1024 bs=1024
wput /tmp/test_ftp  ftp://pi:pitally_01234@localhost
curl ftp://localhost/tmp/test_ftp > /dev/null

#router

uci set system.@system[0].hostname='pitally-router'
uci commit system
/etc/init.d/system reload

