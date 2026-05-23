#!/bin/sh
wget -O /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/download/v26.3.27/Xray-linux-64.zip
unzip /tmp/xray.zip -d /tmp/xray
mv /tmp/xray/xray /usr/local/bin/xray
chmod +x /usr/local/bin/xray
rm -rf /tmp/xray /tmp/xray.zip
