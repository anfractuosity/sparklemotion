# sparklemotion

Simple python program for the Pi using picamera, to record motion to disk

Made from examples I found, such as https://picamera.readthedocs.io/en/release-1.12/recipes2.html

It runs as a system service via sparkle.service.  Additionally I also created hack.service, so that the Pi Noir camera, functions
correctly using the latest Pi firmware in Buster.

# Installation

To build the package and install it:

```
dpkg-deb --build sparklemotion
sudo apt install ./sparklemotion.deb 
```

To start the service:

```
sudo systemctl enable hack
sudo systemctl enable sparklemotion
sudo systemctl start hack
sudo systemctl start sparklemotion
```

To try to save a little power

```
sudo systemctl enable no_usb
sudo systemctl enable no_hdmi
sudo systemctl start no_usb
sudo systemctl start no_hdmi
```

I'm currently having a few issues with the camera on the Pi Zero and am testing
the following:

```
over_voltage=2
force_turbo=1
```
# Example config.toml file

```
[camera]
width = 1280
height = 720
hflip = true
vflip = true

[motion]
mean_threshold = 10.0
vector_threshold = 500

[videos]
path = "/home/pi/vids"
```

# ToDo

* Error checking (check vids folder exists, create if necessary)
* Implement motion detection via little doppler radar module
* Upload video files somewhere via SSH, probably using Paramiko 

