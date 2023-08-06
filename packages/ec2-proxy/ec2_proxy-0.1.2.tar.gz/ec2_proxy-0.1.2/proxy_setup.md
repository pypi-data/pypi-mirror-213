[Source](https://github.com/snail007/goproxy) </br>

```
sudo su
curl -L https://raw.githubusercontent.com/snail007/goproxy/master/install_auto.sh | sudo bash
sudo echo "[Unit]
Description=Proxy server
Requires=network.target
 
[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart="/usr/bin/proxy http -t tcp -p '0.0.0.0:46642'"
TimeoutSec=15
Restart=always
 
[Install]
WantedBy=multi-user.target" > /etc/systemd/system/proxy.service

sudo systemctl daemon-reload
sudo systemctl enable proxy.service
sudo systemctl start proxy.service
sudo systemctl status proxy.service --no-pager
```
</br>
This will install a proxy server that hosts on port 46642. </br>