#!/usr/bin/env bash


if [[ $* == *--enable-service* ]]
then
    echo "[Unit]
    Description=Drive concatenate tool
    Wants=bftpd.service
    After=bftpd.service

    [Service]
    Type=simple
    Environment="FAKE_PITALLY='True'"
    ExecStart=$(which python3) $(which concat_video_chunks.py)
    RestartSec=5
    Restart=always

    [Install]
    WantedBy=multi-user.target" > /etc/systemd/system/pitally_concat.service
##################################################################################

    systemctl daemon-reload
    systemctl enable pitally_concat.service
    systemctl restart pitally_concat.service
fi



