# sparklemotion

Simple python program for the Pi using picamera, to record motion to disk or provide a live stream.

Made from examples I found, such as https://picamera.readthedocs.io/en/release-1.12/recipes2.html

It runs as a system service, which you need to enable and start.

# Installation

To build the package and install it:

```
dpkg-deb --build sparklemotion
sudo apt install ./sparklemotion.deb 
```

Edit /etc/sparklemotion/config.toml if necessary to alter resolution, thresholds for video to be recorded etc.

To start the service:

```
sudo systemctl enable hack
sudo systemctl start hack

sudo systemctl enable sparklemotion
sudo systemctl start sparklemotion
```

To try to save a little power

```
sudo systemctl enable no_usb
sudo systemctl start no_usb

sudo systemctl enable no_hdmi
sudo systemctl start no_hdmi
```

I'm currently having a few issues with the camera on the Pi Zero and am testing
the following, for increased stability:

```
over_voltage=2
force_turbo=1
```

# To Do

* Error checking (check vids folder exists, create if necessary)
* Implement motion detection via little doppler radar module
* Upload video files somewhere via SSH, probably using Paramiko 

