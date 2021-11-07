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
1. The individual nodes (1 per intersection), should recognized the presense of vehicles, be able to count them, and determine their direction relative to the current intersection.
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
  ![Result of Initial TFLite Test](https://github.com/sfagin89/SmartTraffic/blob/main/Object_Detection_Test_1.png?raw=true)
  * A sample TFLite model provided by Google was used as the Detection Model for this test, pulled using the following command:
  ```
  wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip
  ```
  * Some work needs to be done to improve the accuracy. May look into using an accelerator of some kind, as mentioned in the Edje Electronics guide.
  * The data produced by the script still needs to be stored and ready to transmit to other nodes.
### Phase 2 - Node Communication
* How will the Nodes communicate and share traffic information with each other?
  * Considered whether a star topology or a mesh topology wuold work better. A star topology with a central device that communicated with all nodes would allow for a more resource/computationally heavy algorithm. However, this may introduce issues with speed of response times, as traffic information would have to be sent from each node to the central unit, run through an algorithm on that unit, and then sent back to all of the nodes.
  * The current plan is use a partial mesh topology, allowing direct communication between the nodes, as well as providing link redundancy.
* How will Nodes store traffic information received from other nodes?
  * We are treating this similar to how network routers behave, where a routing table is formed based on route information received from other routers, and the best route is determined using a set of metrics dependent on the routing protocol in use. Similarly, the traffic information sent from other nodes will be stored, and the information later used by our Traffic Algortihm to determine the best way to route traffic by adjusting timing of traffic lights.
### Phase 3 - Traffic Adjustment Algorithm
* What algorithm will be used to determine how individual nodes should adjust their traffic light speeds to improve traffic conditions at their own and other intersections?
  * Currently researching existing Traffic Congestion Models, as well as previous research into this topic.[^5][^6][^7]
  * Microscopic traffic flow model vs Macroscopic traffic flow model

## Physical Prototype for Testing Setup
![General Plan for Layout of SmartTraffic System Test](https://github.com/sfagin89/SmartTraffic/blob/main/TrafficIntersectionModel.png?raw=true)
* A minimum of 2 nodes will be needed in order to demonstrate the ability of the nodes to communicate with each other, as well as show how the speeds of the lights will adjust at an intersection based on traffic at another intersection.

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
