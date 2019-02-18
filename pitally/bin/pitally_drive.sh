#!/usr/bin/env bash


if [[ $* == *--enable-service* ]]
then
        echo "[Unit]
        Description=Drive concatenate tool
        Wants=pure-ftpd.service
        After=pure-ftpd.service

        [Service]
        Type=simple
        Environment="FAKE_PITALLY='True'"
        ExecStart=$(which python3) $(which concat_video_chunks.py)
        RestartSec=5
        Restart=always

        [Install]
        WantedBy=multi-user.target" > /etc/systemd/system/pitally_concat.service --cleanup

        echo "[Unit]
        Description=Drive concatenate tool timer

        [Timer]
        OnCalendar=Mon-Sun *-*-* 00:00:00
        OnCalendar=Mon-Sun *-*-* 12:00:00
        Persistent=true

        [Install]
        WantedBy=timers.target" > /etc/systemd/system/pitally_concat.timer

##################################################################################

    systemctl daemon-reload
    systemctl enable pitally_concat.timer
fi



