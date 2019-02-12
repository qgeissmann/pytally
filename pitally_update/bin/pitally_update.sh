#!/usr/bin/env bash


if [[ $* == *--enable-service* ]]
then
    echo "[Unit]
    Description=Pitally update server

    [Service]
    Type=simple
    ExecStart=$(which pitally_update.sh)
    RestartSec=5
    Restart=always

    [Install]
    WantedBy=multi-user.target" > /etc/systemd/system/pitally_update.service

    systemctl daemon-reload
    systemctl enable pitally_update.service
    systemctl restart pitally_update.service
    echo "restarting pitally_update service"
else
    export FLASK_APP=pitally_update && python3 -m flask run --host="0.0.0.0" --port 8080
fi



