# Configuring a Raspberry Pi as a Smart Traffic Node

* It is expected that at least 2 nodes will be configured in order to use the node-to-node communication functionality.

## Hardware Setup

## Software Setup
### Imaging the SD Card:
**IMPORTANT**: This Project uses the RPi OS "Buster", newer OS's have not been confirmed to work.
#### Imaging an SD Card with Raspbian Buster on Windows 10:
* Download Raspbian Buster from the Raspberry Pi Download Site[^12]
  * The version used here is 2021-05-07-raspios-buster-armhf.img
* Unzip the Archived Image
* Insert a blank MicroSD card into your computer
* Use an imaging software to format and image the card
  * The application used to image the card here is Rufus[^13]
  * If the card isn't accessible after the first image, re-image the card.
### Post-Imaging Pre-Boot Setup (Optional Steps):
**All of the following steps should be done within the Boot Folder once the SD card is imaged. None of these steps are required, but they make the first boot of the Pi much simpler**
* Enable SSH by Default
  * Add a plain text file called **SSH**, with no file extension. This file has been provided here in the directory "Files to Add to SD Card Boot Folder Post-Image"
* Manually Connect to Wifi
  * Add a file called **wpa_supplicant.conf**. This file has been provided here in the directory "Files to Add to SD Card Boot Folder Post-Image"
  * Open the file and change "YOUR_NETWORK_NAME" to your wireless network's SSID, and "YOUR_PASSWORD" to your wireless network's password. This setup requires the network you're connecting to to be using WPA-PSK security.
* Adjust Resolution (If using a remote desktop client)
  * Open the file **config.txt**
  * Uncomment the line ```hdmi_force_hotplug=1```
  * Uncomment the line ```hdmi_group=1```
  * Uncomment the line ```hdmi_mode=1 and change the value to 16```
  * Add the following line to the end of the file ```hdmi_ignore_edid=0xa5000080```
### First Boot Setup:
**All of the following steps are done via command line**
* Assuming the Pi is connected to the network, SSH to it using the default username and password for Raspbian
  * Username: Pi
  * Password: raspberry
* Change the default password using the following command:
  * ```passwd```
* Install Updates
  * ```sudo apt-get update```
  * ```sudo apt-get dist-upgrade``` (This can take up to an hour)

**Optional Steps**
* Enable VNC Access
  * Open the Raspbery Pi Config File
    * ```sudo raspi-config```
  * Navigate to Interface Options > VNC
  * Select Yes to enable VNC Server
  * Select Finish
* Set Python3 as default
  * Open the .bashrc file
    * ```nano ~/.bashrc```
  * Type the following on a new line at the end of the file
    * ```alias python=python3```
  * Save and exit the file
  * Run the following command to make the alias permanent
    * ```source ~/.bashrc```

### Installing TensorFlow Lite:
* A guide for Installing and Setting up TensorFlow Lite has been provided by EdjeElectronics[^9]. This guide takes you through installing all of the requirements for running TensorFlow Lite as well.
  * Follow the guide starting at step 1b
  * After downloading the Repo in step 1b, replace the TFLite_detection_webcam.py file with the one in this repo, located in the **Modified files from TFlite Github** directory.
  * In step 1d, Option 1 (Google's sample TFLite model) is used for this project.
* **Once you've finished the setup instructions from the guide, you will need to use the command ```source tflite1-env/bin/activate``` every time you open a new terminal window, or restart the Pi.

### Setting up Ad-Hoc Network between Nodes
* Wired Ad-Hoc Network
  * Connect the Raspberry Pi's together with an ethernet cable
  * Edit the configuration file for the DHCP client daemon on both Pi's
    * ```sudo nano /etc/dhcpcd.conf```
  * Uncomment the following lines:
    * ```interface eth0```
    * ```static ip_address=192.168.0.#/24``` -- Replace # with a number, this number should be different on each node.
    * ```static routers=192.168.0.1```
  * Save and exit the file
  * Restart the Pi's
  * Confirm the static IPs are set by running the following command (2 IPs should now be present):
    * ````
      pi@tnode01:~ $ hostname -I
      192.168.0.10 192.X.X.X
      pi@tnode02:~ $ hostname -I
      192.168.0.20 192.X.X.X
      ````
  * Verify the connection between both nodes by pinging the address of each node from the other.
    * ````
      pi@tnode01:~ $ ping 192.168.0.20
      PING 192.168.0.20 (192.168.0.20) 56(84) bytes of data.
      64 bytes from 192.168.0.20: icmp_seq=1 ttl=64 time=0.618 ms
      64 bytes from 192.168.0.20: icmp_seq=2 ttl=64 time=0.208 ms
      pi@tnode02:~ $ ping 192.168.0.10
      PING 192.168.0.10 (192.168.0.10) 56(84) bytes of data.
      64 bytes from 192.168.0.10: icmp_seq=1 ttl=64 time=0.326 ms
      64 bytes from 192.168.0.10: icmp_seq=2 ttl=64 time=0.197 ms
      64 bytes from 192.168.0.10: icmp_seq=3 ttl=64 time=0.219 ms
      ````
