#!/usr/bin/env bash

GIT_REPO=https://github.com/haneylab/pitally

ZIP_IMG=2018-11-13-raspbian-stretch-lite.zip
RASPBIAN_URL=http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/$ZIP_IMG
PITALLY_IMG_NAME=$(date "+%Y-%m-%d")_pitally_image.img
MOUNT_DIR=/mnt/pitally_root


# if not in chroot
if [ $(systemd-detect-virt) = 'none' ]
then
    set -e
    wget $RASPBIAN_URL -nc
    unzip -o $ZIP_IMG
    mv *raspbian*.img $PITALLY_IMG_NAME
    IMG_FILE=$(ls *.img)
    DEV="$(losetup --show -f -P "$PITALLY_IMG_NAME")"

    mkdir -p $MOUNT_DIR
    mount ${DEV}p2 $MOUNT_DIR
    mount ${DEV}p1 $MOUNT_DIR/boot

    cp $(which qemu-arm-static) ${MOUNT_DIR}/usr/bin
    cp make_image.sh ${MOUNT_DIR}/root/
    chmod +x ${MOUNT_DIR}/root/make_image.sh

    set +e
    systemd-nspawn  --directory ${MOUNT_DIR} /root/make_image.sh

    umount ${DEV}p1
    umount ${DEV}p2
    losetup -d $DEV

else
    touch /boot/ssh
    apt-get update
    apt-get upgrade --assume-yes
    #fixme hack around small image size
    apt-get clean
    apt-get install wput tree ipython3 tcpdump nmap ffmpeg python3-pip iputils-ping git lftp npm --assume-yes
    #fixme hack around small image size
     apt-get clean
    ## the camera and network are enabled when the machine boots for the first time

    ## stack
    git clone $GIT_REPO
    make install -C pitally/
    pitally.sh --enable-service
    pitally_update.sh --enable-service
    rm -rf pitally
    exit
fi
