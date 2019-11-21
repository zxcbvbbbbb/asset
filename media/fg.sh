#!/bin/bash
address = `ip a|grep eth0|grep inet|awk '{print $2}'|awk -F'/' '{print $1}'`

#if [ -d /usr/local/node_exporter ];then echo '目录已存在';set -e;else echo '可以继续安装';fi

cd /usr/local/src
wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1/node_exporter-0.18.1.linux-amd64.tar.gz
tar zxvf node_exporter-0.18.1.linux-amd64.tar.gz
mv node_exporter-0.18.1.linux-amd64 /usr/local/fg_node_exporter

cat > /usr/lib/systemd/system/node_exporter_fg.service <<EOF
[Unit]

[Service]
Restart=on-failure
ExecStart=/usr/local/fg_node_exporter/node_exporter --web.listen-address="$address:19100"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start fg_node_exporter
systemctl status fg_node_exporter