#!/usr/bin/env bash

GIT_REPO=https://github.com/haneylab/pitally
RASPBIAN_URL=http://director.downloads.raspberrypi.org/raspbian_lite/images/raspbian_lite-2018-11-15/2018-11-13-raspbian-stretch-lite.zip

if [[ $* == *--pre-install* ]]
then
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
    CONFIG=/boot/config.txt
    apt-get update
    apt-get upgrade --assume-yes
    apt-get install wput tree ipython3 tcpdump nmap ffmpeg python3-pip iputils-ping git --assume-yes npm

    echo "pi:pitally_01234"|chpasswd

    touch /boot/ssh
    echo "update_config=1
    network={
        ssid="pitally"
        psk="pitally_01234"
    }" >  /etc/wpa_supplicant/wpa_supplicant.conf
    ## camera
    sed s/"INTERACTIVE=True"/"INTERACTIVE=False"/ $(which raspi-config) > /tmp/camera_on.sh && echo "do_camera 1" >> /tmp/camera_on.sh
    sh /tmp/camera_on.sh && rm /tmp/camera_on.sh

    ## stack
    git clone $GIT_REPO
    cd pitally/dist_tarballs

fi
