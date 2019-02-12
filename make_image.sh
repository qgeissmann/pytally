#!/usr/bin/env bash

if [[ $* == *--pre-install* ]]
then
    RASPBIAN_URL=http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip
    #TMP_OUT=$(mktemp -u --suffix '.zip' pitally_image.XXXXXXX)
    ZIP_IMG=image.zip
    MOUNT_DIR=/mnt/pitally_root

    wget -O $ZIP_IMG $RASPBIAN_URL
    unzip $ZIP_IMG
    IMG_FILE=$(ls *.img)
    DEV="$(sudo losetup --show -f -P "$IMG_FILE")"
    #todo if !exist
    sudo mkdir $MOUNT_DIR
    sudo mount ${DEV}p2 $MOUNT_DIR
    sudo mount ${DEV}p1 $MOUNT_DIR/boot

    sudo cp $(which qemu-arm-static) ${MOUNT_DIR}/usr/bin
    sudo cp make_image.sh ${MOUNT_DIR}/root/
    sudo chmod +x ${MOUNT_DIR}/root/make_image.sh
    sudo systemd-nspawn  --directory ${MOUNT_DIR} /root/make_image.sh
else
    apt-get update
    apt-get upgrade --assume-yes
    apt-get install wput tree ipython3 tcpdump nmap ffmpeg python3-pip iputils-ping git --assume-yes

    echo "pi:pitally_01234"|chpasswd
    
fi
