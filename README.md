# SmartTraffic
A System to improve traffic congestion using 'smart' traffic lights

## MVP
A smart traffic light system that is able to recognize, count, and determine the directionality of vehicles at its intersection to create a better traffic route.

## Layout of System
* Each intersection acts as a single 'node'
* Each node is comprised of a controller that connects with 4 cameras
* The 4 cameras are positioned to face each point of ingress to the intersection
* Each node will directly connect to it's neighboring nodes in a mesh network

## A successful finished product should include the following:
1. The individual nodes (1 per intersection), should recognized the presence of vehicles, be able to count them, and determine their direction relative to the current intersection.
2. The nodes should be able to communicate between each other, passing and receiving intersection traffic information.
3. An algorithm that the nodes can use to determine how traffic lights should be adjusted to improve traffic flow in areas of congested traffic, based on the traffic information at their node, as well as all other nodes they hold traffic information for.

## If the above is finished, a reach goal will be attempted:
* Securing the individual nodes and the communication between them to prevent compromised nodes. While security will be taken into account during the main project, additional, redundant security will be considered here.

## Expanding on the above goals
### Phase 1 - Vehicle Recognition
* How will the Intersection node recognize vehicles at its intersection?
  * Google Maps API, or another source of live traffic data was considered. However after looking into how this information is collected and used, and possible ways to abuse the system[^1], we determined to not go with this route.
  * The current plan is to implement Real-Time Object Detection to observe and recognize individual vehicles at each intersection. A set of fisheye lens cameras will be placed at each ingress point of the intersection. Using the feed from these cameras, the individual vehicles will be detected and recognized using the machine learning platform **TensorFlow**[^2].
  * Were considering either the TensorFlow Object Detection API[^3], an open-source framework build on top of TensorFlow, or YOLO TensorFlow ++[^4], a TensorFlow implementation of the YOLO: Real-Time Object Detection algorithm.
* How will the Intersection node determine the directionality of the vehicles?
  * This will be achieved simply by determining which camera is observing the traffic. This becomes more complicated if a single central camera were used.
* Phase 1 Implementation update:
  * Due to using Raspberry Pis as our traffic nodes, the full TensorFlow platform may be too powerful to run effectively. Taking that into account, we have instead gone with **TensorFlow Lite**[^8], an open-source framework built to run on mobile and IoT devices.
  * Using a guide created by **Edje Electronics**[^9][^10] guide, TensorFlow Lite was installed on a Raspberry Pi, along with a simple webcam, and tested on a local street view.
  ![Result of Initial TFLite Test 1](https://github.com/sfagin89/SmartTraffic/blob/main/Object_Detection_Test_1.png?raw=true)
  ![Result of Initial TFLite Test 2](https://github.com/sfagin89/SmartTraffic/blob/main/Object_Detection_Test_2.png?raw=true)
  * A sample TFLite model provided by Google was used as the Detection Model for this test, pulled using the following command:
  ```
  wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
  ```
  * Some work needs to be done to improve the accuracy. May look into using an accelerator of some kind, as mentioned in the Edje Electronics guide. The above test was run using a Raspberry Pi 3. Further implementations will be done on a Raspberry Pi 4, which during benchmark chests has displayed CPU performance improvements of as much as +36%, and GPU performance improvements ranging from +34% - 70% depending on the function being tested[^11]. This increase in CPU and GPU performance should provide significant improvement in the speed and accuracy of the TensorFlow Object Detection.
  * The data produced by the script still needs to be stored and ready to transmit to other nodes.
### Phase 2 - Node Communication
* How will the Nodes communicate and share traffic information with each other?
  * Considered whether a star topology or a mesh topology would work better. A star topology with a central device that communicated with all nodes would allow for a more resource/computationally heavy algorithm. However, this may introduce issues with speed of response times, as traffic information would have to be sent from each node to the central unit, run through an algorithm on that unit, and then sent back to all of the nodes.
  * The current plan is use a partial mesh topology, allowing direct communication between the nodes, as well as providing link redundancy.
* How will Nodes store traffic information received from other nodes?
  * We are treating this similar to how network routers behave, where a routing table is formed based on route information received from other routers, and the best route is determined using a set of metrics dependent on the routing protocol in use. Similarly, the traffic information sent from other nodes will be stored, and the information later used by our Traffic Algorithm to determine the best way to route traffic by adjusting timing of traffic lights.
### Phase 3 - Traffic Adjustment Algorithm
* What algorithm will be used to determine how individual nodes should adjust their traffic light speeds to improve traffic conditions at their own and other intersections?
  * Currently researching existing Traffic Congestion Models, as well as previous research into this topic.[^5][^6][^7]
  * Microscopic traffic flow model vs Macroscopic traffic flow model

## Physical Prototype for Testing Setup
![General Plan for Layout of SmartTraffic System Test](https://github.com/sfagin89/SmartTraffic/blob/main/TrafficIntersectionModel.png?raw=true)
* A minimum of 2 nodes will be needed in order to demonstrate the ability of the nodes to communicate with each other, as well as show how the speeds of the lights will adjust at an intersection based on traffic at another intersection.

## Setting Up the Raspberry Pi as a Traffic Node
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
      ````

## Begin Smart Traffic Application
### Running TensorFlow Lite:
* Run the following command to start Tensorflow Lite:
```python3 TFLite_detection_webcam.py --modeldir=Sample_TFLite_model &```

* To exit the program, run the following commands to kill the process
  ```pgrep python``` The resulting number is the process id
  ```kill -15 <process id>```

* If that doesn't work, use the below as a last resort. This can leave Zombie Processes so isn't ideal.
  ```kill -9 <process id>```

[^1]: https://www.theguardian.com/technology/2020/feb/03/berlin-artist-uses-99-phones-trick-google-maps-traffic-jam-alert
[^2]: https://www.tensorflow.org/
[^3]: https://github.com/tensorflow/models/tree/master/research/object_detection
[^4]: https://modelzoo.co/model/yolo-tensorflow
[^5]: https://iopscience.iop.org/article/10.1088/1742-6596/801/1/012048/pdf
[^6]: https://link.springer.com/referenceworkentry/10.1007%2F978-0-387-30440-3_559#howtocite
[^7]: https://en.wikipedia.org/wiki/Traffic_model
[^8]: https://www.tensorflow.org/lite
[^9]: https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Raspberry_Pi_Guide.md
[^10]: https://www.youtube.com/watch?v=aimSGOAUI8Y&ab_channel=EdjeElectronics
[^11]: https://www.geeks3d.com/20190930/raspberry-pi-4-vs-raspberry-pi-3-cpu-and-gpu-benchmarks/
[^12]: https://downloads.raspberrypi.org/raspios_armhf/images/
[^13]: https://rufus.ie/en/
