# sparklemotion

Simple python program for the Pi using picamera, to record motion to disk

Made from examples I found, such as https://picamera.readthedocs.io/en/release-1.12/recipes2.html

It runs as a system service via sparkle.service.  Additionally I also created hack.service, so that the Pi Noir camera, functions
correctly using the latest Pi firmware in Buster.

# Installation

```
sudo apt-get install python3-numpy
sudo apt-get install python3-pip
sudo pip3 install picamera
mkdir /home/pi/vids

cp sparkle.py /home/pi

sudo cp *.service /etc/systemd/system
sudo systemctl enable hack
sudo systemctl start hack
sudo systemctl enable sparkle
sudo systemctl start sparkle
```
I'm currently having a few issues with the camera on the Pi Zero and am testing
the following:

```
over_voltage=2
force_turbo=1
```

# ToDo

* Error checking (check vids folder exists, create if necessary)
* Implement motion detection via little doppler radar module 

