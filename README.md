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
### Vehicle Recognition
* How will the Intersection node recognize vehicles at its intersection?
  * Google Maps API, or another source of live traffic data was considered. However after looking into how this information is collected and used, and possible ways to abuse the system[^1], we determined to not go with this route.
  * The current plan is to implement Real-Time Object Detection to observe and recognize individual vehicles at each intersection. A set of fisheye lens cameras will be placed at each ingress point of the intersection. Using the feed from these cameras, the individual vehicles will be detected and recognized using the machine learning platform **TensorFlow**[^2].
  *  Currently considering either the TensorFlow Object Detection API[^3], an open-source framework build on top of TensorFlow, or YOLO TensorFlow ++[^4], a TensorFlow implementation of the YOLO: Real-Time Object Detection algorithm.
* How will the Intersection node determine the directionality of the vehicles?
  * This will be achieved simply by determining which camera is observing the traffic. This becomes more complicated if a single central camera were used.
### Node Communication
* How will the Nodes communicate and share traffic information with each other?
* How will Nodes store traffic information received from other nodes?
### Traffic Adjustment Algorithm
* What algorithm will be used to determine how individual nodes should adjust their traffic light speeds to improve traffic conditions at their own and other intersections?

## Physical Prototype for Testing Setup
![General Plan for Layout of SmartTraffic System Test](https://github.com/sfagin89/SmartTraffic/blob/main/TrafficIntersectionModel.png?raw=true)
* A minimum of 2 nodes will be needed in order to demonstrate the ability of the nodes to communicate with each other, as well as show how the speeds of the lights will adjust at an intersection based on traffic at another intersection.

[^1]: https://www.theguardian.com/technology/2020/feb/03/berlin-artist-uses-99-phones-trick-google-maps-traffic-jam-alert
[^2]: https://www.tensorflow.org/
[^3]: https://github.com/tensorflow/models/tree/master/research/object_detection
[^4]: https://modelzoo.co/model/yolo-tensorflow
