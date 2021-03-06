#install playsound
python3 -m pip install playsound
apt install python3-gst-1.0

# create the systemd service
touch /etc/systemd/system/portal.service
cd /etc/systemd/system/
echo "[Unit]" >> portal.service
echo "Descrpition=Portal Service" >> portal.service
echo "After=mutli-user.target" >> portal.service
echo "" >> portal.service
echo "[Service]" >> portal.service
echo "Type=idle" >> portal.service
echo "Restart=always" >> portal.service
echo "ExecStart=/usr/bin/python3 /home/pi/portal-rpi/portal.py" >> portal.service
echo "" >> portal.service
echo "[Install]" >> portal.service
echo "WantedBy=multi-user.target" >> portal.service
systemctl daemon-reload
systemctl enable portal.service
systemctl start portal.service
