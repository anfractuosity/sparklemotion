# sparklemotion

Simple python program for the Pi using picamera, to record motion to disk

Made from examples I found, such as https://picamera.readthedocs.io/en/release-1.12/recipes2.html

# Installation

```
sudo apt-get install python3-numpy
sudo apt-get install python3-pip
sudo pip3 install picamera
mkdir /home/pi/vids

cp sparkle.py /home/pi

sudo cp sparkle.service /etc/systemd/system
sudo systemctl enable sparkle
sudo systemctl start sparkle
```

```
over_voltage=2
force_turbo=1
```

