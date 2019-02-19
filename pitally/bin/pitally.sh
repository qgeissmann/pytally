#!/usr/bin/env bash


if [[ $* == *--enable-service* ]]
then
##################################################################################
echo "[Unit]
Description=Pitally server
#Wants=ntpd.service
#After=ntpd.service


[Service]
Type=simple
#WorkingDirectory=/opt/ethoscope-git/node_src/scripts
ExecStart=$(which pitally.sh)
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/pitally.service
##################################################################################
echo "[Unit]
Description=Pitally backup server
#Wants=ntpd.service
#After=ntpd.service

[Service]
Type=simple
Environment="FAKE_PITALLY='True'"
ExecStart=$(which python3) $(which pitally_backup.py)
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/pitally_backup.service
##################################################################################

    systemctl daemon-reload
    systemctl enable pitally.service
    systemctl enable pitally_backup.service
    systemctl restart pitally.service
    systemctl restart pitally_backup.service
    echo "restarting pitally services"
else
    export FLASK_APP=pitally && python3 -m flask run --host="0.0.0.0" --port 80
fi



