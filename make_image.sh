#!/usr/bin/env bash

GIT_REPO=https://github.com/haneylab/pitally
RASPBIAN_URL=http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip
PITALLY_IMG_NAME=$(date "+%Y-%m-%d")_pitally_image.img
MOUNT_DIR=/mnt/pitally_root

if [[ $* == *--pre-install* ]]
#todo if in a chroot =>
#if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]
then
    #TMP_OUT=$(mktemp -u --suffix '.zip' pitally_image.XXXXXXX)
    ZIP_IMG=image.zip

    wget -O $ZIP_IMG $RASPBIAN_URL
    unzip -o $ZIP_IMG && rm $ZIP_IMG
    mv raspbian*.img $PITALLY_IMG_NAME
    IMG_FILE=$(ls *.img)
    DEV="$(losetup --show -f -P "$IMG_FILE")"
    #todo if !exist
    mkdir -p $MOUNT_DIR
    mount ${DEV}p2 $MOUNT_DIR
    mount ${DEV}p1 $MOUNT_DIR/boot

    cp $(which qemu-arm-static) ${MOUNT_DIR}/usr/bin
    cp make_image.sh ${MOUNT_DIR}/root/
    chmod +x ${MOUNT_DIR}/root/make_image.sh
        systemd-nspawn  --directory ${MOUNT_DIR} /root/make_image.sh

    umount ${DEV}p1
    umount ${DEV}p2
    losetup -d $DEV

else
    CONFIG=/boot/config.txt
    apt-get update
    apt-get upgrade --assume-yes
    apt-get install wput tree ipython3 tcpdump nmap ffmpeg python3-pip iputils-ping git npm --assume-yes

    echo "pi:pitally_01234"|chpasswd

    touch /boot/ssh

echo "
network={
    ssid="pitally"
    psk="pitally_01234"
}" >>  /etc/wpa_supplicant/wpa_supplicant.conf

    ## camera
    sed s/"INTERACTIVE=True"/"INTERACTIVE=False"/ $(which raspi-config) > /tmp/camera_on.sh && echo "do_camera 1" >> /tmp/camera_on.sh
    sh /tmp/camera_on.sh && rm /tmp/camera_on.sh

    ## stack
    git clone $GIT_REPO
    make install -C pitally/
    pitally.sh --enable-service
    pitally_update.sh --enable-service
    rm -rf pitally
    exit
fi
